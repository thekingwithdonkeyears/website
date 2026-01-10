require 'yaml'
require 'fileutils'
require 'set'

# Configuration
POSTS_DIR = '_posts'
TAGS_DIR = '_pages/tag'
LAYOUT = 'tag'

# Ensure output directory exists
FileUtils.mkdir_p(TAGS_DIR)

# Collect all tags
tags = Set.new

puts "Scanning posts in #{POSTS_DIR}..."

Dir.glob("#{POSTS_DIR}/**/*.md").each do |post_file|
  content = File.read(post_file)
  if content =~ /\A(---\s*\n.*?\n?)^(---\s*$\n?)/m
    front_matter = YAML.load($1)
    if front_matter['tags']
      # Tags can be a string or array, normalize to array
      post_tags = front_matter['tags'].is_a?(String) ? front_matter['tags'].split : front_matter['tags']
      tags.merge(post_tags)
    end
  end
end

puts "Found #{tags.size} unique tags."

# Generate tag pages
tags.each do |tag|
  # Sanitize tag for filename (optional, but good practice if tags have weird chars)
  # For now, assuming tags are safe for filenames or already URL encoded if needed.
  # Using the tag directly as per user's category approach.
  
  filename = File.join(TAGS_DIR, "#{tag}.md")
  
  # Skip if file already exists? User wants to "really create", maybe overwrite is better.
  # Let's overwrite to ensure consistency.
  
  File.open(filename, 'w') do |f|
    f.puts "---"
    f.puts "layout: #{LAYOUT}"
    f.puts "title: #{tag}"
    f.puts "permalink: /tag/#{tag}/"
    f.puts "---"
  end
end

puts "Generated #{tags.size} tag pages in #{TAGS_DIR}."
