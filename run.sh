folder_path=pcap
output_folder_base=output

mkdir -p "$output_folder_base"

for file_name in "$folder_path"/*; do
    if [ -f "$file_name" ]; then
        file_name=$(basename "$file_name")
        output_folder=$(echo "$file_name" | awk -F '_' '{print $1}')
        
        mkdir -p "$output_folder_base/$output_folder"
        echo -e "\nFile: $file_name"
        echo -e "Output: $output_folder_base/$output_folder"

        python pcap2img.py --pcap "$folder_path/$file_name" --output "$output_folder_base/$output_folder" --width 28 --height 28
    fi
done