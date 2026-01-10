require 'uri'

# Configuration
POSTS_DIR = '_posts/fanfic'
TARGET_DOMAIN = 'https://fanfic.thekingwithdonkeyears.com'
OUTPUT_FILE = '_redirects'

puts "Generating redirects..."

File.open(OUTPUT_FILE, 'w') do |f|
  # Add a comment header
  f.puts "# Redirects for Fanfic posts moving to subdomain"
  
  Dir.glob("#{POSTS_DIR}/*.md").each do |post_file|
    filename = File.basename(post_file, '.md')
    
    # Extract slug from filename: YYYY-MM-DD-slug
    if filename =~ /^\d{4}-\d{2}-\d{2}-(.*)$/
      slug = $1
      
      # The source path on the old site
      source_path = "/#{slug}/"
      
      # The target URL on the new site
      # Assuming the structure is preserved
      target_url = "#{TARGET_DOMAIN}/#{slug}/"
      
      # Cloudflare _redirects format: /source-path target-url status
      f.puts "#{source_path} #{target_url} 301"
      
      # Also add entry without trailing slash just in case
      f.puts "/#{slug} #{target_url} 301"
    end
  end
end

puts "Done. Redirects written to #{OUTPUT_FILE}"
