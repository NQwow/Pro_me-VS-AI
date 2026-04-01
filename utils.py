def get_int_input(prompt, min=0, max=100):
    while True:
        try:
            value = int(input(prompt))
            if min<= value <= max:
                return value
            else:
                print(f"数值必须在 {min} 到 {max} 之间，请重新输入。")
        except ValueError:
            print("输入无效，请输入一个0-100间的整数。")