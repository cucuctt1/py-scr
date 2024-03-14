
def start_parse(stack):
    code = ""
    for item in stack.controls:
        print(stack.controls)
        if item.IsHeader:
            for item in item.below_code:
                #print(item)
                code += item.code_parser() + "\n"
                print(code)
            exec(code)
            break