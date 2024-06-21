import os


def read_js_file(file_path):
    with open(file_path, "r") as file:
        data = file.read()
    return data


def create_basic_program(txt_lines, start_line):
    basic_lines = []
    line_number = start_line
    remaining_txt_lines = []

    for js_line in txt_lines:
        if "{" in js_line or "}" in js_line:
            continue
        escaped_js_line = js_line.replace('"', '""')
        if line_number > 9970:
            remaining_txt_lines = txt_lines[txt_lines.index(js_line) :]
            basic_lines.append(f'{line_number} PRINT "END OF CHUNK"')
            break
        basic_lines.append(f'{line_number} PRINT "{escaped_js_line}"')
        line_number += 10

    if not remaining_txt_lines and line_number <= 9970:
        basic_lines.append(f'{line_number} PRINT "END OF FILE"')
        line_number += 10
    basic_lines.append(f"{line_number} STOP")
    return "\r\n".join(basic_lines) + "\r\n", remaining_txt_lines


def save_basic_program(basic_program, bas_file_path):
    with open(bas_file_path, "w") as bas_file:
        bas_file.write(basic_program)


def split_js_to_bas(js_file_path, output_dir, name):
    js_data = read_js_file(js_file_path)
    txt_lines = js_data.split("\n")
    chunk_number = 1
    start_line = 10

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while txt_lines:
        bas_file_path = os.path.join(output_dir, f"{name}_{chunk_number}.bas")
        basic_program, txt_lines = create_basic_program(txt_lines, start_line)
        save_basic_program(basic_program, bas_file_path)
        print(f"BASIC program saved to: {bas_file_path}")
        chunk_number += 1


def compile_bas_to_tap(output_dir):
    bas_files = [f for f in os.listdir(output_dir) if f.endswith(".bas")]
    chunk_number = 1
    for bas_file in bas_files:
        bas_file_path = os.path.join(output_dir, bas_file)
        tap_file_path = os.path.join(output_dir, bas_file.replace(".bas", ".tap"))
        os.system(f"./bas2tap {bas_file_path} -a")
        print(f"TAP file created: {tap_file_path}")
        os.system(f"./zxtap2wav -i {tap_file_path}")
        chunk_number += 1


output_dir = "output"

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python main.py <file_path> <name>")
        sys.exit(1)
    file_path = sys.argv[1]
    name = sys.argv[2]
    split_js_to_bas(file_path, output_dir, name)
    compile_bas_to_tap(output_dir)
