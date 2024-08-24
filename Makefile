.PHONY: preview
preview:
	@echo "monitoring markdown changes..."
	@reflex -r '\.md' -R docs make all

all:
	@echo "changes detected, rebuilding the blog..." 
	@go run .
