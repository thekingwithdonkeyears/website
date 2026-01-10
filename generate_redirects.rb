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
    
    if filename =~ /^(\d{4})-(\d{2})-(\d{2})-(.*)$/
      year, month, day, slug = $1, $2, $3, $4
      
      # Target is always the subdomain (assuming subdomain setup supports /:slug/ or matches source)
      # If the target subdomain actually follows /:slug/, we keep it simple.
      target_url = "#{TARGET_DOMAIN}/#{URI.encode_www_form_component(slug)}/"
      
      # We need to generate multiple variations to catch old incoming links
      
      # 1. Date-based path (Old Jekyll default): /YYYY/MM/DD/slug/
      # We must URI encode the source path too, especially for Chinese
      encoded_slug = URI.encode_www_form_component(slug)
      
      # Variation A: /YYYY/MM/DD/slug/
      f.puts "/#{year}/#{month}/#{day}/#{encoded_slug}/ #{target_url} 301"
      f.puts "/#{year}/#{month}/#{day}/#{encoded_slug} #{target_url} 301"

      # Variation B: /slug/ (Current config default)
      f.puts "/#{encoded_slug}/ #{target_url} 301"
      f.puts "/#{encoded_slug} #{target_url} 301"

      # Variation C: Lowercase slug (for case insensitive matching)
      if slug != slug.downcase
        lower_slug = URI.encode_www_form_component(slug.downcase)
        f.puts "/#{year}/#{month}/#{day}/#{lower_slug}/ #{target_url} 301"
        f.puts "/#{year}/#{month}/#{day}/#{lower_slug} #{target_url} 301"
        f.puts "/#{lower_slug}/ #{target_url} 301"
        f.puts "/#{lower_slug} #{target_url} 301"
      end
    end
  end
end

puts "Done. Redirects written to #{OUTPUT_FILE}"
