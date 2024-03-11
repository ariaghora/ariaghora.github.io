package main

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/yuin/goldmark"
	"github.com/yuin/goldmark/extension"
	"github.com/yuin/goldmark/renderer/html"
	"gopkg.in/yaml.v2"
)

const ConfigFile = "config.yaml"

type Config struct {
	InputDir  string `yaml:"input_dir"`
	OutputDir string `yaml:"output_dir"`
	Header    string `yaml:"header"`
	Footer    string `yaml:"footer"`
}

type TwitterMeta struct {
	Title       string `yaml:"title,omitempty"`
	Description string `yaml:"description,omitempty"`
	Image       string `yaml:"image,omitempty"`
}

type Meta struct {
	Twitter *TwitterMeta `yaml:"twitter,omitempty"`
}

func LoadConfig() (*Config, error) {
	// Check if config file exists

	file, err := os.Open(ConfigFile)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	// Read config file
	decoder := yaml.NewDecoder(file)
	var config *Config = &Config{}
	err = decoder.Decode(config)
	if err != nil {
		return nil, err
	}

	return config, nil
}

// ReadTextFile reads a markdown file and returns its content as a string.
func ReadTextFile(path string) (string, error) {
	file, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer file.Close()

	// Read file
	content, err := io.ReadAll(file)
	if err != nil {
		return "", err
	}

	return string(content), nil
}

func PreprocessMarkdown(markdown string) string {
	// Convert markdown links to HTML links
	pattern := regexp.MustCompile(`\[(.*)\]\((.*)\.md\)`)
	output := pattern.ReplaceAllString(markdown, "[$1]($2.html)")
	return output
}

// Compile a markdown string into HTML string
func CompileMarkdown(markdown string) (string, error) {
	if len(strings.TrimSpace(markdown)) == 0 {
		return "", nil
	}

	// Preprocess markdown
	markdown = PreprocessMarkdown(markdown)

	var buf bytes.Buffer

	md := goldmark.New(
		goldmark.WithExtensions(
			extension.Table,
			extension.Footnote,
		),
		goldmark.WithRendererOptions(
			html.WithUnsafe(),
		),
	)
	err := md.Convert([]byte(markdown), &buf)
	if err != nil {
		return "", err
	}

	return buf.String(), nil
}

func WriteHTMLFile(path string, html string) error {
	// Create output directory if it does not exist
	outputDir := filepath.Dir(path)
	err := os.MkdirAll(outputDir, os.ModePerm)
	if err != nil {
		return err
	}

	file, err := os.Create(path)
	if err != nil {
		return err
	}
	defer file.Close()

	_, err = file.WriteString(html)
	if err != nil {
		return err
	}

	return nil
}

func CopyFile(src, dst string) error {
	bytesRead, err := os.ReadFile(src)
	if err != nil {
		return err
	}

	err = os.WriteFile(dst, bytesRead, 0644)
	if err != nil {
		return err
	}

	return nil
}

func CompileMeta(meta *Meta) string {
	twitterTitle := ""
	twitterDesc := ""
	twitterImage := ""
	if meta.Twitter != nil {
		if len(meta.Twitter.Title) > 0 {
			twitterTitle = fmt.Sprintf("<meta name=\"twitter:title\" content=\"%s\">\n", meta.Twitter.Title)
		}
		if len(meta.Twitter.Description) > 0 {
			twitterDesc = fmt.Sprintf("<meta name=\"twitter:description\" content=\"%s\">\n", meta.Twitter.Description)
		}
		if len(meta.Twitter.Image) > 0 {
			twitterImage = fmt.Sprintf("<meta name=\"twitter:image\" content=\"%s\">\n", meta.Twitter.Image)
		}
	}
	return fmt.Sprintf("%s%s%s", twitterTitle, twitterDesc, twitterImage)
}

func CompileWebsite(config *Config) error {
	inputDir := config.InputDir
	outputDir := config.OutputDir
	headerFile := config.Header
	footerFile := config.Footer

	// Remove output directory if it exists. Remove all files and subdirectories.
	err := os.RemoveAll(outputDir)
	if err != nil {
		return err
	}

	// Check if output directory exists. If not, create it.
	err = os.MkdirAll(outputDir, os.ModePerm)
	if err != nil {
		return err
	}

	// Walk through input directory and list markdown files
	err = filepath.Walk(inputDir, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if info.IsDir() && strings.Contains(info.Name(), "venv") {
			return filepath.SkipDir
		}

		if info.IsDir() {
			return nil
		}

		if filepath.Ext(path) != ".md" {
			// just copy the file as is
			// Create the directory if it does not exist.
			// The output directory is the same as the input directory, but with the output directory as the root.
			fileOutputDir := filepath.Join(outputDir, strings.TrimPrefix(filepath.Dir(path), inputDir))
			if err = os.MkdirAll(fileOutputDir, os.ModePerm); err != nil {
				return err
			}

			relPath, err := filepath.Rel(inputDir, path)
			if err != nil {
				return err
			}

			outputPath := filepath.Join(outputDir, relPath)
			if err := CopyFile(path, outputPath); err != nil {
				return err
			}
		} else {
			// Compile markdown file
			markdown, err := ReadTextFile(path)
			if err != nil {
				return err
			}

			html, err := CompileMarkdown(markdown)
			if err != nil {
				return err
			}

			metaPath := fmt.Sprintf("%s/%s", filepath.Dir(path), "meta.yaml")
			metaStr, _ := ReadTextFile(metaPath)
			metaHtml := ""
			if len(metaStr) > 0 {
				meta := &Meta{}
				err = yaml.Unmarshal([]byte(metaStr), meta)
				if err == nil {
					metaHtml = CompileMeta(meta)
				}
			}

			// Add header and footer
			htmlHeader, err := ReadTextFile(headerFile)
			if err != nil {
				return err
			}

			htmlFooter, err := ReadTextFile(footerFile)
			if err != nil {
				return err
			}
			html = htmlHeader + html + htmlFooter
			html = strings.Replace(html, "{{social_meta}}", metaHtml, 1)

			// Write HTML file; Replace prefix of input directory with output directory
			outputPath := filepath.Join(strings.TrimSuffix(path, ".md") + ".html")
			outputPath = strings.Replace(outputPath, inputDir, outputDir, 1)

			return WriteHTMLFile(outputPath, html)
		}
		return nil
	})

	return err
}

func main() {
	config, err := LoadConfig()
	if err != nil {
		fmt.Println("configuration error:", err)
		os.Exit(1)
	}

	err = CompileWebsite(config)
	if err != nil {
		fmt.Println("compilation error:", err)
		os.Exit(1)
	}

}
