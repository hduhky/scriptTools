#!/usr/bin/ruby -w
# -*- coding: UTF-8 -*-
$items_dic = {}
$duplicate_dic = {}

def duplicate_check_for_folder(folder_path)
  Dir.foreach(folder_path) do |file|
    if file == "." or file == ".." or file == ".DS_Store"
      next
    end
    path = File.join(folder_path, file)
    if File.directory? path
      if $items_dic.has_key?file
        if $duplicate_dic.has_key?file
          path_list = $duplicate_dic[file].to_ary
          path_list.append(path)
        else
          path_list = [$items_dic[file], path]
          $duplicate_dic[file] = path_list
        end
      else
        $items_dic[file] = path
      end
      duplicate_check_for_folder(path)
    end
  end
end

if __FILE__ == $0
  first_file = ARGV[0]

  if first_file.nil?
    first_file = "/Users/smb-lsp/Desktop/Switch/trunk_ezlive_switch/ios/EZViewer/Images.xcassets"
  end
  duplicate_check_for_folder(first_file)
  $duplicate_dic.each_value do |value|
    arr = value.to_ary
    arr.map do |path|
      path.slice! first_file
    end
  end
  $duplicate_dic.each do |key, value|
    puts "#{key}=>#{value}\n\n"
  end
end