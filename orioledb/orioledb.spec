
# These are macros to be used with find_lang and other stuff
%global sname orioledb
%global pgbaseinstdir	/usr/pgsql-%{pgmajorversion}
%{!?test:%global test 1}

%ifarch ppc64 ppc64le s390 s390x armv7hl
%{!?sdt:%global sdt 0}
%else
 %{!?sdt:%global sdt 1}
%endif

%{!?selinux:%global selinux 1}

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if 0%{?fedora} > 30
%global _hardened_build 1
%endif

%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch ppc64 ppc64le
%pgdg_set_ppc64le_compiler_at10
%endif
%endif

Summary:	OrioleDB is a new storage engine for PostgreSQL, bringing a modern approach to database capacity, capabilities and performance to the world's most-loved database platform.
Name:		postgres%{pgmajorversion}-%{sname}
Version:	%{gittag}
Release:	orioledb%{?dist}
License:	PostgreSQL
Url:		%{url}

#https://github.com/orioledb/postgres/archive/refs/tags/patches16_22.tar.gz
Source0:        %{source0}
Source1:        setenv

BuildRequires:  libzstd-devel
BuildRequires:	postgresql%{pgmajorversion}-devel
BuildRequires:	libcurl-devel

Requires:       libzstd
Requires:	oriolepg%{pgmajorversion}-server


%description
OrioleDB is a new storage engine for PostgreSQL, bringing a modern approach to database capacity, capabilities and performance to the world's most-loved database platform.
OrioleDB consists of an extension, building on the innovative table access method framework and other standard Postgres extension interfaces.
By extending and enhancing the current table access methods, OrioleDB opens the door to a future of more powerful storage models that are optimized for cloud and modern hardware architectures.

OrioleDB delivers the following added value:
- OrioleDB design avoids legacy CPU bottlenecks on modern servers containing dozens and hundreds CPU cores, providing optimized usage of modern storage technologies such as SSD and NVRAM.
- OrioleDB implements the concepts of undo log and page-mergins, eliminating the need for dedicated garbage collection processes. Additionally, OrioleDB implements default 64-bit transaction identifiers, thus eliminating the well-known and painful wraparound problem.
- OrioleDB implements a row-level write-ahead log with support for parallel apply. This log architecture is optimized for raft consensus-based replication allowing the implementation of active-active multimaster.

The following key technical differentiations of OrioleDB make this happen:
- No buffer mapping and lock-less page reading. In-memory pages in OrioleDB are connected with direct links to the storage pages. This eliminates the need for in-buffer mapping along with its related bottlenecks. Additionally, in OrioleDB in-memory page reading doesn't involve atomic operations. Together, these design decisions bring vertical scalability for Postgres to the whole new level.
- MVCC is based on the UNDO log concept. In OrioleDB, old versions of tuples do not cause bloat in the main storage system, but eviction into the undo log comprising undo chains. Page-level undo records allow the system to easily reclaim space occupied by deleted tuples as soon as possible. Together with page-mergins, these mechanisms eliminate bloat in the majority of cases. Dedicated VACUUMing of tables is not needed as well, removing a significant and common cause of system performance deterioration and database outages.
- Copy-on-write checkpoints and row-level WAL. OrioleDB utilizes copy-on-write checkpoints, which provides a structurally consistent snapshot of data every moment of time. This is friendly for modern SSDs and allows row-level WAL logging. In turn, row-level WAL logging is easy to parallelize (done), compact and suitable for active-active multimaster (planned).


%prep
pwd
%{__rm} -rf %{_builddir}/*

tar -xvf %{SOURCE0}
mv */* .
cp %{SOURCE1} .

%build
. ./setenv
%{__make} USE_PGXS=1

%install
%{__rm} -rf %{buildroot}

. ./setenv
%{__make} DESTDIR=%{buildroot} USE_PGXS=1 install

%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root)
%doc LICENSE
%{pgbaseinstdir}/lib/bitcode/orioledb.index.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/btree.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/build.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/check.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/find.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/insert.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/io.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/iterator.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/merge.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/modify.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/page_chunks.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/page_contents.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/page_state.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/print.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/scan.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/split.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/btree/undo.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/ddl.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/free_extents.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/indices.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_aggregate_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_amop_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_amproc_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_class_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_collation_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_database_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_enum_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_indices.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_opclass_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_operator_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_proc_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_range_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_sys_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_tables.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/o_type_cache.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/catalog/sys_trees.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/checkpoint/checkpoint.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/orioledb.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/recovery/recovery.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/recovery/wal.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/recovery/worker.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/archive.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/checkpoint.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/headers.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/queue.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/requests.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/s3/worker.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/bitmap_scan.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/descr.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/func.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/handler.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/index_scan.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/key_bitmap.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/key_range.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/operations.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/scan.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tableam/tree.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/transam/oxid.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/transam/undo.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tuple/format.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tuple/slot.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tuple/sort.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/tuple/toast.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/compress.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/o_buffers.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/page_pool.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/planner.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/seq_buf.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/stopevent.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/utils/ucm.bc
%{pgbaseinstdir}/lib/bitcode/orioledb/src/workers/bgwriter.bc
%{pgbaseinstdir}/lib/orioledb.so
%{pgbaseinstdir}/share/extension/orioledb*


%changelog
* Sat Feb 3 2024 Sebastiaan Mannem <sebas@mannemsolutions.nl> alpha1 spec
- Initial spec for building OrioleDB extension

