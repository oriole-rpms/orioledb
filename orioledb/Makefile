all: clean configure build copy

clean:
	rm -rf ~/rpmbuild

configure:
	./configure.sh

build:
	rpmbuild -ba "./orioledb.spec"

copy:
	mkdir -p rpms
	find ~/rpmbuild -name '*.rpm' -exec cp {} rpms/ \;
