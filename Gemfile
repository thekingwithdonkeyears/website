# Frozen_string_literal: true
Encoding.default_external = Encoding::UTF_8
Encoding.default_internal = Encoding::UTF_8

source "https://rubygems.org"

# gem "jekyll"  # Commented out to avoid conflict with github-pages gem which pins Jekyll version
gem "webrick"   # 避免 Jekyll 4.2.0 以上的版本出錯
gem "csv"

# 如果你要部署到 GitHub Pages，請加入：
group :jekyll_plugins do
  gem "github-pages", "~> 228", group: :jekyll_plugins
end
gem "jekyll-archives", "~> 2.2"
