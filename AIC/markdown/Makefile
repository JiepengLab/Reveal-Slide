.PHONY: live build clean

live:
	@echo "Previewing main slides..."
	-@reveal-md main.md

build:
	@echo "Building main slides..."
	@reveal-md main.md --static .. --assets-dir assets

clean:
	@echo "Cleaning up..."
	rm -rf ../site/
