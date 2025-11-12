run:
	python3 orbit.py

install: clean get_dependency build
	# TODO: move needed files to bin

build: clean
	pyinstaller --onefile --hidden-import=lib --add-data ".env:."  orbit.py

get_dependency:
	pip install -r requirements.txt

clean:
	rm -r build/ dist/ orbit.spec