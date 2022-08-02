import os
import json
import shutil

def replaceText(directory, filesNames, oldText, newText):
    for fileName in filesNames:
        somefile = open(directory + "/" + fileName, "r")
        textFile = somefile.read()
        newTextFile = textFile.replace(oldText, newText)
        somefile.close()

        somefile = open(directory + "/" + fileName, "w")
        somefile.write(newTextFile)
        somefile.close()


class My_json:
    def str_to_dict(self, string):
        return json.loads(string)
    def dict_to_str(self, dictionary):
        return json.dumps(dictionary)

    def set_dict_file(self, filename, dictionary):
        with open(filename, 'w') as file:
            json.dump(dictionary, file)
    def get_dict_file(self, filename):
        with open(filename, 'r') as file:
            return json.load(file)


class Gen:
    def __init__(self):
        self.json = My_json()
        self.config = self.json.get_dict_file("./config.json")

    def get_input_names(self):
        files = os.listdir(self.config["dir_input"])
        return list(filter(lambda x: x[-5:] == '.html', files))
    def get_template_names(self):
        files = os.listdir(self.config["dir_templates"])
        return list(filter(lambda x: x[-5:] == '.html', files))
    def get_other_names(self):
            return os.listdir(self.config["dir_input"])

    def generate(self):
        # All files
        print(f"[1/3] Start coping files")
        for other_name in self.get_other_names():
            src = f"{self.config['dir_input']}"
            dst = f"{self.config['dir_output']}"
            shutil.copytree(src, dst, dirs_exist_ok=True)
        print(f"[1/3] Stop coping files")

        # Templates
        print(f"[2/3] Start templates")
        for input_name in self.get_input_names():
            input_file = open(f"{self.config['dir_input']}/{input_name}", "r")
            text_file = input_file.read()

            # Templates
            for template_name in self.get_template_names():
                template_file = open(f"{self.config['dir_templates']}/{template_name}", "r")
                text_file = text_file.replace("{{" + template_name.split(".")[0] + "}}", template_file.read())
                template_file.close()

            # Version
            text_file = text_file.replace("{{version}}", f"{self.config['version']}")

            input_file.close()
            output_file = open(f"{self.config['dir_output']}/{input_name}", "w")
            output_file.write(text_file)
            output_file.close()
        print(f"[2/3] Stop templates")
        print(f"[3/3] Current version: {self.config['version']}")

        self.config['version'] += 1
        self.json.set_dict_file("./config.json", self.config)



gen = Gen()
gen.generate()
