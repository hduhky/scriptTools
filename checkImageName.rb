#!/usr/bin/ruby -w
# -*- coding: UTF-8 -*-
$searchName = "\"trailing\""
$replaceName = "\"right\""

def image_name_check_for_folder(folder_path)
  Dir.foreach(folder_path) do |file|
    if file == "." or file == ".." or file == ".DS_Store"
      next
    end
    path = File.join(folder_path, file)
    if File.directory? path
      image_name_check_for_folder(path)
    else
      if path.include? ".xib" or path.include? ".storyboard"
        text = File.read(path)
        if text.include? $searchName
         replace = text.gsub($searchName, $replaceName)
         File.open(path, "w") do |target_file|
           target_file.puts replace
          end
        end
      end
    end
  end
end

if __FILE__ == $0
  first_file = ARGV[0]

  if first_file.nil?
    first_file = "/Users/smb-lsp/Desktop/Switch/trunk_ezlive_switch/ios/"
  end
  image_name_check_for_folder(first_file)

  puts("image_name_check_for_folder Done!")
end