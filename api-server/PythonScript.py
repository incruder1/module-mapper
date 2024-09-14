import os
import time
import json
import sys
# import for ollama
from langchain_community.llms import Ollama
# import for groq
from langchain_groq import ChatGroq




#===============================================================CLASSES DEFINED================================================
class FileStructure:
    def __init__(self, file_path, file_name, file_content):
        self.file_path = file_path
        self.file_name = file_name
        self.file_content = file_content

class ClassEntity:
    def __init__(self, ClassName, ClassExtendsName, ClassImplementsName, ClassParentFilePath):
        self.ClassName = ClassName
        self.ClassExtendsName = ClassExtendsName if ClassExtendsName is not None else None
        self.ClassImplementsName = ClassImplementsName if ClassImplementsName is not None else None
        self.ClassParentFilePath = ClassParentFilePath

    def __str__(self):
        return f"ClassName: {self.ClassName}, ClassExtendsName: {self.ClassExtendsName}, ClassImplementsName: {self.ClassImplementsName}, ClassParentFilePath: {self.ClassParentFilePath}"

    def __eq__(self, other):
        if not isinstance(other, ClassEntity):
            return NotImplemented
        return (self.ClassName == other.ClassName and 
                self.ClassExtendsName == other.ClassExtendsName and 
                self.ClassImplementsName == other.ClassImplementsName and 
                self.ClassParentFilePath == other.ClassParentFilePath)

class FieldEntity:
    def __init__(self, field_name, field_type):
        self.field_name = field_name
        self.field_type = field_type

    def __str__(self):
        return f"Field Name: {self.field_name}, Field Type: {self.field_type}"

    def __eq__(self, other):
        if not isinstance(other, FieldEntity):
            return NotImplemented
        return (self.field_name == other.field_name and self.field_type == other.field_type)


class ModelEntity:
    def __init__(self, Name, Fields=None):
        self.Name = Name
        # Initialize Fields as an empty list if None is provided
        if Fields is None:
            self.Fields: list[FieldEntity] = []
        else:
            self.Fields = Fields

    def __str__(self):
        # Handle the string representation of the list of FieldEntity objects
        field_str = ', '.join(str(field) for field in self.Fields)
        return f"Name: {self.Name}, Fields: [{field_str}]"
    
    def __eq__(self, other):
        if not isinstance(other, ModelEntity):
            return NotImplemented
        # Check equality by comparing name and all fields in the list
        return (self.Name == other.Name and self.Fields == other.Fields)

    def add_field(self, field):
        # Append a new FieldEntity to the Fields list
        if isinstance(field, FieldEntity):
            self.Fields.append(field)
        else:
            raise TypeError("Only FieldEntity instances can be added")

class FileEntity:
    def __init__(self, FileName, FilePath, FileType):
        self.FileName = FileName
        self.FilePath = FilePath
        self.FileType = FileType

    def __str__(self):
        return f"FileName: {self.FileName}, FilePath: {self.FilePath}, FileType: {self.FileType}"

    def __eq__(self, other):
        if not isinstance(other, FileEntity):
            return NotImplemented
        return (self.FileName == other.FileName and self.FilePath == other.FilePath and self.FileType == other.FileType)
    
class MethodsEntity:
    def __init__(self, FilePath, MethodName, MethodClassName, EndPointUrl=None):
        self.FilePath = FilePath
        self.MethodName = MethodName
        self.MethodClassName = MethodClassName
        self.EndPointUrl = EndPointUrl  # This attribute is now optional

    def __str__(self):
        return f"FilePath: {self.FilePath}, MethodName: {self.MethodName}, MethodClassName: {self.MethodClassName}, EndPointUrl: {self.EndPointUrl if self.EndPointUrl else 'Not Specified'}"

    def __eq__(self, other):
        if not isinstance(other, MethodsEntity):
            return NotImplemented
        return (self.FilePath == other.FilePath and 
                self.MethodName == other.MethodName and 
                self.MethodClassName == other.MethodClassName and 
                (self.EndPointUrl == other.EndPointUrl if self.EndPointUrl and other.EndPointUrl else True))

class CallingMethod:
    """
    Represents the details of a method that is calling another method.
    """
    def __init__(self, file_path: str, class_name: str, method_name: str):
        self.file_path = file_path
        self.class_name = class_name
        self.method_name = method_name

    def __str__(self) -> str:
        return (f"Method Details:\n"
                f"File Path: {self.file_path}\n"
                f"Class Name: {self.class_name}\n"
                f"Method Name: {self.method_name}")

class ReceivingMethod:
    """
    Represents the details of a method that is receiving a call.
    This class allows for the file path to be optional.
    """
    def __init__(self, file_path: str, class_name: str, method_name: str):
        self.file_path = file_path  # This can be None if no file path is provided
        self.class_name = class_name
        self.method_name = method_name

    def __str__(self) -> str:
        return (f"Function Details:\n"
                f"File Path: {self.file_path if self.file_path is not None else 'Not Provided'}\n"
                f"Class Name: {self.class_name}\n"
                f"Method Name: {self.method_name}")

class SendRecEntity:
    """
    Represents a single interaction between a calling method and a receiving method.
    """
    def __init__(self, calling_method: CallingMethod, receiving_method: ReceivingMethod):
        self.calling_method = calling_method
        self.receiving_method = receiving_method

    def __str__(self) -> str:
        return (f"Interaction Details:\n"
                f"Calling Method:\n{self.calling_method}\n"
                f"Receiving Method:\n{self.receiving_method}")

class GraphNode:
    def __init__(self, name: str, attributes: dict, children: list = None) -> None:
        self.name = name
        self.attributes = attributes
        self.children = children if children is not None else []

    def to_dict(self):
        graph_dic = {
            "name": self.name,
            "attributes": self.attributes,
        }
        if self.children:
            graph_dic['children'] = [child.to_dict() for child in self.children]
        
        return graph_dic

# ======================================================== LLM =============================================================


#Initializing the Ollama Deepseekcoder Model

# local_llm = Ollama(
#     model = "deepseek-coder-v2:16b-lite-instruct-q4_K_M"
# )

#initializing the Groq llm
groq_llm = ChatGroq(verbose=True, temperature=0, groq_api_key="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", model_name="mixtral-8x7b-32768")
# groq_llm = ChatGroq(verbose=True, temperature=0, groq_api_key="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", model_name="llama3-8b-8192")




# ======================================================== VARIABLE DECLARATION ================================================


list_of_files = []
json_data = []
string_json_from_llm = []

file_entities: list[FileEntity] = []
class_entities: list[ClassEntity] = []
model_entities: list[ModelEntity] = []
method_entities: list[MethodsEntity] = []
send_rec_entities: list[SendRecEntity] = []

class_map = {}
file_map = {}
model_map = {}
method_map = {}

interface_entities = []


class_entities_json = []
method_entites_json = []
file_entities_json = []
model_entities_json = []
function_called_entities_json = []


#=============================================================== FUNCTIONS ===========================================================




# function to read through the directory and identify the required files by prompting the llm and store it in list_of_files
def print_file_names(directory_url):
    print(f'$$ STARTED GOING THROUGH THE DIRECTORY: {directory_url}')

    programming_file_formats = ['.c', '.cpp', '.cs', '.java', '.js', '.py', '.php', '.rb', '.swift', '.go', '.ts', '.kt', '.m', '.swift', '.rs', '.rs', '.dart', '.scala', '.pl', '.rb', '.sh', '.sql']
    for i, str in enumerate(programming_file_formats):
        programming_file_formats[i] = str[1:]

    
    file_count = 0
    try:
        for root, dirs, files in os.walk(directory_url):
            for file_name in files:
                if file_name.split('.')[-1] in programming_file_formats and not root.__contains__('node_modules'):
                    flag = False
                    for dir_name in root.split('\\'):
                        if len(dir_name) > 0 and dir_name[0] == '.':
                            flag = True
                    if flag:
                        continue
                    file_count += 1
    except Exception as e:
        print(e)
        pass

    print(f'\nTotal Files spotted in the project: {file_count}\n')
    if file_count == 0:
        print('Exiting...')
        return 'Empty Directory'
    
    processed_files = 1

    try:
        for root, dirs, files in os.walk(directory_url):
            for file_name in files:
                if file_name.split('.')[-1] in programming_file_formats and not root.__contains__('node_modules'):
                    flag = False
                    for dir_name in root.split('\\'):
                        if len(dir_name) > 0 and dir_name[0] == '.':
                            flag = True
                    if flag:
                        continue
                    print(f'\n-------------------------\nFile {processed_files} of {file_count}...')
                    processed_files += 1

                    file_name = file_name.replace('\\', '/')

                    print(f'FileName: {file_name}')
                    try:
                        with open(root + "/" + file_name, 'r') as f:
                            file_path = (f"{root}/{file_name}").replace("\\","/")
                            file_content = f.read()

                            startTime = time.time()

                            llm_decision = groq_llm.invoke(
    f"""
    System: 
    ```
    You are a helpful code analyzing assistant.
    We are working on a project which will create a Link diagram which is similar to a UML diagram with files, classes and methods represented as Nodes and function calls between them represented as uni-directional arrows/edges between them.
    The Aim of the project is to help developers easily understand the function calls between different files in a repository by visualizing the diagram.

    Your TASK: To identify/decide if the given file is actually useful for our project like a Controller, Database Model/Entity or DTO, Service, queue definition or any other similar important file with core logic written and necessary for creating of the Project mapping, \nlike a configuration file, a test file or a migration file might not be neccessary to consider for our project. 
    You only reply in ONE WORD, which is either "YES" or "NO".
    ```

    Human:
    ```
    File Path: {file_path}
    File Name: {file_name}
    File Content: \n{rf"{file_content}"}\n
    ```
    """
                            )
                            endTime = time.time()
                            print(f'Time taken by LLM to decide: {endTime - startTime:.2f} seconds.')

                            if llm_decision.content.lower().__contains__("yes"):
                                current_file_structure = FileStructure(file_path=file_path, file_name=file_name, file_content=file_content)
                                list_of_files.append(current_file_structure)
                                print(f"{file_name} created!")
                            else:
                                print(f"{file_name} skipped...")
                    except Exception as e:
                        print(f"Encountered an exception while opening the file: {file_path}")
                        print(e)
    except Exception as e:
        print(f"Encountered an exception while walking the directory: {directory_url}")
        print(e)
    print('\n$$ FINISHED GOING THROUGH THE DIRECTORY')
    print(f'No of files, llm considered: {len(list_of_files)}\n')



# list to store the llm output
list_of_all_llm_outputs = []

# function to extract the node information from the file. The whole file is sent to the llm to analyze and extract the required node information
def extract_nodes_form_the_file(list_of_files):
    print('\n$$ STARTED PROMPTING LLM TO EXTRACT JSON DATA\n')
    try:
        for file in list_of_files:
            llm_output = groq_llm.invoke( 
"""
You are a helpful code analyzing assistant who understands the code provided and recognises the flow of the project and identify if there is a connection between the given file and another file without assuming anything out of the file. Assume you are being given one whole file at a time without any code being left out for that file.
Input : You will be given the file name code in it and the path.
Your Task : You have to extract the data based on the given below condition and provide a output in JSON format without any additional context or explanations. 
You will be provided the file_path, file_name and the file_content which will be a code in one of the programming language.

Your Job is to identify if the folowing json pattern is present, if yes fill it and add the same to your output , if not do not add that particular json pattern.
Remember you might have to give multiple json patterns in most of the case.
Output format: JSON (no explanation for your reply), starts with '{' and ends with '}'

The patterns that you should find is given below:
Remember the following:

a. If any of the below section is not present in the given code then do not add that section in the output.
b. When you are getting the details of the methods called in the section 5, if there are any inbuilt functions provided by the language library, ignore those functions. 
c. A file can either be a model or a class, not both
d. If there is a nested class present in the file given consider the nested calss as a new class node and represent it in the JSON format. 
e. While mentioning the methodNames, only write the method parameters type, do not include the variable names anywhere or the default values

1. Enter the Details of the given File.

"File" : 
{
    "FileName": name of the file,
    "FilePath": path of the file,
    "FileType": identify the functionality of the file which might be [RestAPIController, Service, Model/Entity/DTO, Database Repository, Interface, Class, Anonymous]. Use anonymous when none of the other category fits.
}

2. Analyze if the given code is of type Model/Entity/DTO if yes extract the below information.
"Models" : 
[
    {
        "Name": name of model/dto/entity/..,
        "Fields":
        [
            {
                "field_name": name of the field,
                "field_type": datatype of the field
            }
        ],
        "FilePath": path of the file
    },
]

3. Identify the classes present in the given code, if present extract the details of each class.  
"Classes" : 
[
    {
        "ClassName": name of the class,
        "ClassExtendsName": if it extends any other class then list of class name else null,
        "ClassImplementsName": if it implements any interface then list of interface name else null,
        "ClassParentFilePath": path of the file where the class exists
    },
]
    
4. check if there are methods in the in the file if yes extract the details of each method present in the given code.
"MethodsDefined" : 
[
    {
        "FilePath": path of the file where the method exists,
        "MethodClassName": name of the class where method is declared,
        "MethodName": name of the method with its parameters signature in (),
        "EndPointUrl": if any endpoint url exists else null,
    },
]

5. Identify functions which is been called inside the method or anywhere else in the code which might be reffering to a different file in a project.
"FunctionsCalled" : 
[
    {
        "DetailsOfCallingMethod": {
            "FilePath": path of the current file,
            "ClassName": class inside the current file from which the function has been called, may be null,
            "MethodName": Name of the defined method along with parameters signature in () from which the other function has been called, may be null
        },
        "DetailsOfFunctionBeingCalled": {
            "FilePath": null,
            "ClassName": class name or the module name where the called function exists, try to find it in the import section of the file or the object type, if you can't find or not applicable then null, if the calling object is an alias, fill the actual module/package name
            "MethodName": Name of the function/method with its parameters signature in ()
        }
    },
]

Analyze the given below input and do not include any text
INPUT:
""" + f"""
File Name- {file.file_name}
File Path- {file.file_path}
File Content-
{rf"{file.file_content}"}
""")
            print(llm_output.content)
            print(llm_output.content.replace(r'\_', '_'))
            list_of_all_llm_outputs.append(llm_output.content.replace(r'\_', '_'))
            print(f"{len(list_of_all_llm_outputs) = }")
    except Exception as e:
        print(f"LLM Exception: {e}")
        extract_nodes_form_the_file(list_of_files[len(list_of_all_llm_outputs):])
    print('\n$$ FINISHED PROMPTING LLM TO EXTRACT JSON DATA\n')



# Function to check existence and add new FileEntity
def add_file_entity(file_info):
    new_entity = FileEntity(file_info['FileName'], file_info['FilePath'], file_info['FileType'])
    if new_entity not in file_entities:
        file_entities.append(new_entity)
        print(f"Added new FileEntity: {new_entity.FileName}")
    else:
        print("FileEntity already exists in the list.")


def add_model_entity(name, fields):
    # Ensure that all items in fields are instances of FieldEntity
    if not all(isinstance(field, FieldEntity) for field in fields):
        raise ValueError("All fields must be instances of FieldEntity")

    # Create a new ModelEntity with the provided name and fields
    new_entity = ModelEntity(name, fields)

    # Check if the new entity already exists in the list of model entities
    if new_entity not in model_entities:
        model_entities.append(new_entity)
        print(f"Added new ModelEntity: {new_entity.Name}")
    else:
        print("ModelEntity already exists in the list.")




# Function to check existence and add new MethodsEntity
def add_methods_entity(file_path, method_name, method_class_name, end_point_url=None):
    new_method_entity = MethodsEntity(file_path, method_name, method_class_name, end_point_url)
    if new_method_entity not in method_entities:
        method_entities.append(new_method_entity)
        print(f"Added new MethodsEntity: {new_method_entity.MethodName}")
    else:
        print("MethodsEntity already exists in the list.")




# Function to check existence and add new ClassEntity
def add_class_entity(class_name, class_extends_name, class_implements_name, class_parent_file_path):
    new_class_entity = ClassEntity(class_name, class_extends_name, class_implements_name, class_parent_file_path)
    if new_class_entity not in class_entities:
        class_entities.append(new_class_entity)
        class_map[class_name]=len(class_entities)-1
        print(f"Added new ClassEntity: {new_class_entity.ClassName}")
    else:
        print("ClassEntity already exists in the list.")




def add_send_rec_entity(calling_method, receiving_method):
    """
    Function to check existence and add new SendRecEntity.
    Args:
    calling_method (CallingMethod): The calling method details.
    receiving_method (ReceivingMethod): The receiving method details.
    """
    # Create a new SendRecEntity with the provided calling and receiving methods
    new_send_rec_entity = SendRecEntity(calling_method, receiving_method)

    # Check if the new entity already exists in the list of send_rec_entities
    if new_send_rec_entity not in send_rec_entities:
        send_rec_entities.append(new_send_rec_entity)
        print(f"Added new SendRecEntity: {new_send_rec_entity.calling_method.method_name} -> {new_send_rec_entity.receiving_method.method_name}")
    else:
        print("SendRecEntity already exists in the list.")


# Function which Loops through all the json data and create the respective python object
def create_python_objects_from_json_data():
    global string_json_from_llm
    for data in string_json_from_llm:
        # Check if 'file' key exists in the data dictionary
        if 'File' in data:
            add_file_entity(data['File'])  # Ensure the key matches the expected structure
            
        if 'Models' in data:
                # Assuming 'json_data' is a dictionary loaded from JSON that contains the model information
            for model in data['Models']:
                # Create a list to hold FieldEntity objects
                field_entities = []
        
                # Convert each field in the model to a FieldEntity
                for field in model['Fields']:
                    field_entity = FieldEntity(field['field_name'], field['field_type'])
                    field_entities.append(field_entity)
        
                # Add the model entity to the list
                add_model_entity(model['Name'], field_entities)

        if 'MethodsDefined' in data:
            for method in data['MethodsDefined']:  # Corrected to 'methods' to match the key in the JSON data
                # Ensure the keys match the expected structure and handle optional 'EndPointUrl'
                add_methods_entity(method['FilePath'], method['MethodName'], method['MethodClassName'], method.get('EndPointUrl'))


        if 'Classes' in data:  # Assuming 'class' could contain multiple classes
            for class_info in data['Classes']:  # Corrected to 'class' to match the key in the JSON data
                # Ensure the keys match the expected structure
                add_class_entity(class_info['ClassName'], class_info.get('ClassExtendsName'), class_info.get('ClassImplementsName'), class_info['ClassParentFilePath'])

        if 'FunctionsCalled' in data:
            for function in data['FunctionsCalled']:

                calling_details = function["DetailsOfCallingMethod"]
                calling_method = CallingMethod(file_path=calling_details["FilePath"],class_name=calling_details["ClassName"],method_name=calling_details["MethodName"])
                receiving_details = function["DetailsOfFunctionBeingCalled"]
                receiving_method = ReceivingMethod(file_path=receiving_details["FilePath"],  class_name=receiving_details["ClassName"],method_name=receiving_details["MethodName"])
                add_send_rec_entity(calling_method, receiving_method)


def get_correct_file_path(class_name: str, method_name: str):
    for entity in method_entities:
        if (((not entity.MethodClassName or entity.MethodClassName == 'None') or (not class_name or class_name == 'None')) or (entity.MethodClassName and entity.MethodClassName.lower() == class_name.lower())) and entity.MethodName.lower() == method_name.lower():
            return entity.FilePath
            


# function which Mapps the method called with method declared
def mapp_the_function_called_with_method_declared():
    for entity in send_rec_entities:
        if entity.receiving_method.file_path is None and entity.receiving_method.method_name:
            entity.receiving_method.file_path = get_correct_file_path(entity.receiving_method.class_name, entity.receiving_method.method_name)

def create_file_object_json():
    with open('mapped/file_obj.json', 'w') as f:
        f.write('[')
        for file in file_entities:
            f.write('\n\t{')
            f.write(f'\n\t\t"FilePath" : "{file.FilePath}",')
            f.write(f'\n\t\t"FileName" : "{file.FileName}",')
            f.write(f'\n\t\t"FileType" : "{file.FileType}"')
            f.write('\n\t}')
            if file_entities.index(file) != len(file_entities) - 1:
                f.write(',')
        f.write('\n]')

def create_model_object_json():
    with open('mapped/model_obj.json', 'w') as f:
        f.write('[')
        for model in model_entities:
            f.write('\n\t{')
            f.write(f'\n\t\t"Name" : "{model.Name}",')
            f.write(f'\n\t\t"Fields" : ')
            f.write('[')

            for field in model.Fields:
                f.write('\n\t\t\t{')
                f.write(f'\n\t\t\t\t"field_name" : "{field.field_name}",')
                f.write(f'\n\t\t\t\t"field_type" : "{field.field_type}"')
                f.write('\n\t\t\t}')
                if model.Fields.index(field) != len(model.Fields) - 1:
                    f.write(',')
            f.write('\n\t\t]')
            f.write('\n\t}')
            if model_entities.index(model) != len(model_entities) - 1:
                f.write(',')
        f.write('\n]')
    
def create_methods_defined_json():
    with open('mapped/method_defined_obj.json', 'w') as f:
        f.write('[')
        for method in method_entities:
            f.write('\n\t{')
            f.write(f'\n\t\t"FilePath" : "{method.FilePath}",')
            f.write(f'\n\t\t"MethodClassName" : "{method.MethodClassName}",')
            f.write(f'\n\t\t"MethodName" : "{method.MethodName}",')
            f.write(f'\n\t\t"EndPointUrl" : "{method.EndPointUrl}"')
            f.write('\n\t}')
            if method_entities.index(method) != len(method_entities) - 1:
                f.write(',')
        f.write('\n]')

def create_class_object_json():
    with open('mapped/class_obj.json', 'w') as f:
        f.write('[')
        for cls in class_entities:
            f.write('\n\t{')
            f.write(f'\n\t\t"ClassParentFilePath" : "{cls.ClassParentFilePath}",')
            f.write(f'\n\t\t"ClassName" : "{cls.ClassName}",')

            if isinstance(cls.ClassExtendsName, str):
                f.write(f'\n\t\t"ClassExtendsName" : "{cls.ClassExtendsName}",')
            elif isinstance(cls.ClassExtendsName, list):
                f.write(f'\n\t\t"ClassExtendsName" : [')
                for entry in cls.ClassExtendsName:
                    f.write(f'\n\t\t\t"{entry}"')
                    if cls.ClassExtendsName.index(entry) != len(cls.ClassExtendsName) - 1:
                        f.write(',')
                f.write('\n\t\t],')
            elif cls.ClassExtendsName is None:
                f.write('\n\t\t"ClassExtendsName" : "None",')

            if isinstance(cls.ClassImplementsName, str):
                f.write(f'\n\t\t"ClassImplementsName" : "{cls.ClassImplementsName}"')
            elif isinstance(cls.ClassImplementsName, list):
                f.write(f'\n\t\t"ClassImplementsName" : [')
                for entry in cls.ClassImplementsName:
                    f.write(f'\n\t\t\t"{entry}"')
                    if cls.ClassImplementsName.index(entry) != len(cls.ClassImplementsName) - 1:
                        f.write(',')
                f.write('\n\t\t]')
            elif cls.ClassImplementsName is None:
                f.write('\n\t\t"ClassImplementsName" : "None"')
                    
            f.write('\n\t}')
            if class_entities.index(cls) != len(class_entities) - 1:
                f.write(',')
        f.write('\n]')

def create_function_called_object_json():
    global send_rec_entities
    global function_called_entities_json

    last_ind = None
    for send_rec in send_rec_entities[::-1]:
        if send_rec.receiving_method.file_path is not None:
            last_ind = send_rec_entities.index(send_rec)
            break

    with open('mapped/function_called_obj.json', 'w') as f:
        f.write('[')
        for send_rec in send_rec_entities:
            if send_rec.receiving_method.file_path is None:
                continue
            f.write('\n\t{')
            
            f.write('\n\t\t"calling_method" : {')
            f.write(f'\n\t\t\t"file_path" : "{send_rec.calling_method.file_path}",')
            f.write(f'\n\t\t\t"class_name" : "{send_rec.calling_method.class_name}",')
            f.write(f'\n\t\t\t"method_name" : "{send_rec.calling_method.method_name}"')
            f.write('\n\t\t},')

            f.write('\n\t\t"receiving_method" : {')
            f.write(f'\n\t\t\t"file_path" : "{send_rec.receiving_method.file_path}",')
            f.write(f'\n\t\t\t"class_name" : "{send_rec.receiving_method.class_name}",')
            f.write(f'\n\t\t\t"method_name" : "{send_rec.receiving_method.method_name}"')
            f.write('\n\t\t}')
            
            f.write('\n\t}')
            if send_rec_entities.index(send_rec) != last_ind:
                f.write(',')
        f.write('\n]')


def generate_mapped_jsons():
    dir_name = 'mapped'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f'Directory "{dir_name}" created.')
    else:
        print(f'Directory "{dir_name}" already exists.')

    create_file_object_json()
    create_class_object_json()
    create_model_object_json()
    create_methods_defined_json()
    create_function_called_object_json()


# Function to read the files in model folder
def read_json_and_classify_data_from_model_folder():
    global class_entities_json
    global method_entites_json
    global file_entities_json
    global model_entities_json
    global function_called_entities_json

    with open('mapped/class_obj.json') as f:
        class_entities_json = json.loads(f.read())

    interface_entities = []

    for cls in class_entities_json:
        if isinstance(cls['ClassImplementsName'], list):
            for implements_name in cls['ClassImplementsName']:
                if implements_name == cls['ClassName']:
                    cls['ClassImplementsName'].remove(implements_name)
                    continue
                for innerCls in class_entities_json:
                    if innerCls['ClassName'] == implements_name:
                        # class_entities.remove(innerCls)
                        interface_entities.append(innerCls)
                            
    with open('mapped/method_defined_obj.json') as f:
        method_entites_json = json.loads(f.read())
    with open('mapped/file_obj.json') as f:
        file_entities_json = json.loads(f.read())
    with open('mapped/model_obj.json') as f:
        model_entities_json = json.loads(f.read())
    with open('mapped/function_called_obj.json') as f:
        function_called_entities_json = json.loads(f.read())





def generate_json_for_mermaid(url):
    repo_name = url

    base_dic = GraphNode(
        name="Repo#A", 
        attributes={
            "Type": "Directory",
            "Path": repo_name
        })

    for file_ind, file in enumerate(file_entities_json):
        file_attributes = {
            "Type": "File",
            "Contains": file['FileType'],
            "Path": file['FilePath']
        }
        file_node = GraphNode(name=file['FileName'], attributes=file_attributes)
        base_dic.children.append(file_node)

        for cls in class_entities_json:
            if cls['ClassParentFilePath'] == file['FilePath']:
                node_type = 'Class'
                for interface in interface_entities:
                    if interface == cls:
                        node_type = 'Interface'

                cls_attributes = {
                    'Type': node_type
                }
                if 'ClassExtendsName' in cls and cls['ClassExtendsName'] != "None":
                    cls_attributes['Extends'] = cls['ClassExtendsName']
                if 'ClassImplementsName' in cls and cls['ClassImplementsName'] != "None":
                    cls_attributes['Implements'] = cls['ClassImplementsName']
                
                for model in model_entities_json:
                    if model['Name'] == cls['ClassName']:
                        cls_attributes['Fields'] = [f"{field['field_name']} {field['field_type']}" for field in model['Fields']]

                cls_attributes['Path'] = cls['ClassParentFilePath']

                cls_node = GraphNode(name=cls['ClassName'], attributes=cls_attributes)
                file_node.children.append(cls_node)

                for method in method_entites_json:
                    if method['FilePath'] == cls['ClassParentFilePath'] and method['MethodClassName'] == cls['ClassName']:

                        method_attributes = {
                            'Type': 'Method'
                        }
                        if 'EndPointUrl' in method and method['EndPointUrl'] != "None":
                            method_attributes['EndPoint URL'] = method['EndPointUrl']

                        method_node = GraphNode(name=method['MethodName'], attributes=method_attributes)
                        cls_node.children.append(method_node)

                        for function_call in function_called_entities_json:
                            send_func = function_call['calling_method']
                            rec_func = function_call['receiving_method']

                            if send_func['method_name'] == method['MethodName'] and send_func['class_name'] == method['MethodClassName'] and send_func['file_path'] == file['FilePath']:
                                
                                function_call_attributes = {
                                    'Type': 'Function Call'
                                }
                                if rec_func['class_name'] != 'None':
                                    function_call_attributes['Class'] = rec_func['class_name']
                                function_call_attributes['Path'] = rec_func['file_path']

                                function_call_node = GraphNode(name=rec_func['method_name'], attributes=function_call_attributes)

                                method_node.children.append(function_call_node)
                                            
        for method in method_entites_json:
            if method['MethodClassName'] == 'None' and method['FilePath'] == file['FilePath']:
                method_attributes = {
                    'Type': 'Method'
                }
                if 'EndPointUrl' in method and method['EndPointUrl'] != "None":
                            method_attributes['EndPoint URL'] = method['EndPointUrl']

                method_node = GraphNode(name=method['MethodName'], attributes=method_attributes)

                file_node.children.append(method_node)

                for function_call in function_called_entities_json:
                            send_func = function_call['calling_method']
                            rec_func = function_call['receiving_method']

                            if send_func['method_name'] == method['MethodName'] and send_func['class_name'] == method['MethodClassName'] and send_func['file_path'] == file['FilePath']:
                                
                                function_call_attributes = {
                                    'Type': 'Function Call'
                                }
                                if rec_func['class_name'] != 'None':
                                    function_call_attributes['Class'] = rec_func['class_name']
                                function_call_attributes['Path'] = rec_func['file_path']

                                function_call_node = GraphNode(name=rec_func['method_name'], attributes=function_call_attributes)

                                method_node.children.append(function_call_node)
        for function_call in function_called_entities_json:
            send_func = function_call['calling_method']
            rec_func = function_call['receiving_method']

            if send_func['method_name'] == 'None' and send_func['class_name'] == 'None' and send_func['file_path'] == file['FilePath']:
                function_call_attributes = {
                    'Type': 'Function Call'
                }
                if rec_func['class_name'] != 'None':
                    function_call_attributes['Class'] = rec_func['class_name']
                function_call_attributes['Path'] = rec_func['file_path']

                function_call_node = GraphNode(name=rec_func['method_name'], attributes=function_call_attributes)

                file_node.children.append(function_call_node)

    with open('antd_data.json', 'w') as t:
        t.write(json.dumps(base_dic.to_dict(), indent=2))


# Generete Mermaid
def generate_mermaid():
    with open('mapped/class_obj.json') as f:
        class_entities = json.loads(f.read())

    interface_classes = []

    for cls in class_entities:
        if isinstance(cls['ClassImplementsName'], list):
            for implements_name in cls['ClassImplementsName']:
                if implements_name == cls['ClassName']:
                    cls['ClassImplementsName'].remove(implements_name)
                    continue
                for innerCls in class_entities:
                    if innerCls['ClassName'] == implements_name:
                        # class_entities.remove(cls)
                        interface_classes.append(innerCls)

    with open('mapped/method_defined_obj.json') as f:
        method_entites = json.loads(f.read())

    with open('mapped/file_obj.json') as f:
        file_entities = json.loads(f.read())

    with open('mapped/model_obj.json') as f:
        model_entities = json.loads(f.read())

    with open('mapped/function_called_obj.json') as f:
        function_called_entities = json.loads(f.read())


    mermaid_code = 'classDiagram\n\ndirection LR\n'

    method_ref_name_dic = {}

    file_class_added = set()

    for cls in class_entities:
        # if cls['ClassName'] not in ['BookingController', 'BookingServiceImpl', 'BookingService']:
            # continue
        # if class_entities.index(cls) == 2:
        #     break

        this_is_an_interface = False
        if cls in interface_classes:
            this_is_an_interface = True
            
        cls_flag = False

        for file in file_entities:
            if file['FilePath'] == cls['ClassParentFilePath']:
                if file['FileType'].lower().__contains__('model'):
                    cls_flag = True
                    break

                filename = f"\\`{file['FileName']}\\`"

                filepath = file['FilePath'].split('/')
                filepath = f".../{'/'.join(filepath[-2:])}"

                if filename in file_class_added:
                    break
                
                mermaid_code += f'''
        class {filename} ''' + '{' + '''
            ''' + f'''Type: File
            Contains: {file['FileType']}
            Path: {filepath}
        ''' + '}\n'
                
                file_class_added.add(filename)
        
        if cls_flag:
            continue

        if isinstance(cls['ClassImplementsName'], list):
            for implementationName in cls['ClassImplementsName']:
                implementationName = f"\\`{implementationName}\\`"
                mermaid_code += f'''
                    class {implementationName} '''+ '''{
                    }''' + f'''

                    {cls['ClassName']} ..|> {implementationName} : Implements
                '''
        
        class_obj_type = 'Interface' if this_is_an_interface else 'Class'

        mermaid_code += f'''
        class {cls['ClassName']}''' + '''{
            ''' + f'''Type: {class_obj_type}
            FileName: {cls["ClassParentFilePath"].split('/')[-1]}
        ''' + '}' + f'''

        {filename} --|> {cls['ClassName']} : Defines
        '''

        for method in method_entites:
            if method['FilePath'] == cls['ClassParentFilePath'] and method['MethodClassName'] == cls['ClassName']:

                meth_name, meth_params = method['MethodName'][:method['MethodName'].index('(')], method['MethodName'][method['MethodName'].index('('):]

                meth_params = meth_params.split(')')[0].split('.')[-1]
                meth_name = meth_name.split(' ')[-1] + f'({meth_params})'

                meth_ref_name = f"\\`{cls['ClassName']}_{meth_name}\\`"

                endpoint = method['EndPointUrl'].replace('{', '~').replace('}', '~')
                
                method_ref_name_dic[f"{method['FilePath'].lower()}-{method['MethodClassName'].lower()}-{method['MethodName'].lower()}"] = cls['ClassName']

                if endpoint and endpoint != 'None':
                    meth_name += f' {endpoint}'

                mermaid_code += f'''
                {cls['ClassName']} : {method['MethodName'].replace(':', '')} {endpoint if endpoint else ''}
                '''

    already_invoked = {}

    for function_called in function_called_entities:
        call_method = function_called['calling_method']
        rec_method = function_called['receiving_method']

        from_method_name = method_ref_name_dic.get(f"{call_method['file_path'].lower()}-{call_method['class_name'].lower()}-{call_method['method_name'].lower()}", None)
        to_method_name = method_ref_name_dic.get(f"{rec_method['file_path'].lower()}-{rec_method['class_name'].lower()}-{rec_method['method_name'].lower()}", None)

        if from_method_name and to_method_name and to_method_name not in already_invoked.get(from_method_name, []):
            mermaid_code += f'''
            {from_method_name} --> {to_method_name} : Invokes
            '''
            if from_method_name not in already_invoked:
                already_invoked[from_method_name] = [to_method_name]
            else:
                already_invoked[from_method_name].append(to_method_name)

    model_mermaid_code = ''
    for model in model_entities:
        # if model_entities.index(model) == 2:
        #     break
        
        for file in file_entities:
            if file['FileType'].lower().__contains__('model') and file['FileName'].split('.')[0].lower() == model['Name'].lower():
                filename = f"\\`{file['FileName']}\\`"
                
                filepath = file['FilePath'].split('/')
                filepath = f".../{'/'.join(filepath[-2:])}"
                
                model_mermaid_code += f'''
        class {filename} ''' + '{' + '''
            ''' + f'''Type: File
            Contains: {file['FileType']}
            Path: {filepath}
        ''' + '}\n'
                
        fields = '[\n'
                
        for obj in model['Fields']:
            fields += f'''\n{obj['field_type'].replace('<', '~').replace('>', '~')} {obj['field_name']}\n'''
        fields += ']'

        model_mermaid_code += f'''
        class {model['Name']} ''' + '{' + '''
            ''' + f'''Type: Class
            Fields: {fields}
        ''' + '}' + f'''

        {filename} --|> {model['Name']} : Defines
        '''

    dir_name = 'mermaid_code'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    with open(f'{dir_name}/graph.js', 'w') as f:
        f.write(f'export default `\n{mermaid_code}\n\n{model_mermaid_code}\n`')
    
    with open(f'{dir_name}/graph.md', 'w') as f:
        f.write(f'```mermaid\n{mermaid_code}\n\n{model_mermaid_code}\n```'.replace(r'\`', '`'))


# main function
def read_directory(url):
    global string_json_from_llm
    url = url.replace("\\", '/')

    if not os.path.exists(url):
        print('Invalid Path!')
        return "Invalid Directory Path!"

    #Extracting the required files
    try:
        res_of_print_dir = print_file_names(url)
        if res_of_print_dir == 'Empty Directory':
            return res_of_print_dir
    except:
        print("Error in reading the directory")
    
    #Extracting the Node from files
    try:
        extract_nodes_form_the_file(list_of_files)
        with open('results.txt', 'w') as f:
            for i in list_of_all_llm_outputs:
                try:
                    f.write('\n' + "="*100 + '\n')
                    f.write(i)
                except Exception as e:
                    f.write(f'Some ERROR occured: {e.args}')
    except Exception as e:
        print(f"Error in extracting the nodes from the files \n {e}")



    # Reading result.txt file and splitting it with delimitter ("="*100)
    try:
        string_json_from_llm = ['None'] * len(list_of_all_llm_outputs)
        for ind, json_string in enumerate(list_of_all_llm_outputs):
            json_string = json_string.strip()

            open_brace_index = json_string.index('{')
            close_brace_index = json_string.rindex('}')

            try:
                json_data = json.loads(json_string[open_brace_index:close_brace_index + 1].replace(r'\_', '_'))

                string_json_from_llm[ind] = json_data
            except Exception as innerE:
                print(f'Error occured while converting str to json: {innerE}')
                print(f'Telling LLM to fix it...')
                groq_resp = groq_llm.invoke(f'Please fix the json formatting, close any unclosed things: \n\n{json_string[open_brace_index:close_brace_index + 1]}. \n\n Return me only the json, no explanation.').content
                groq_resp = groq_resp.strip()

                open_brace_index = groq_resp.index('{')
                close_brace_index = groq_resp.rindex('}')
                try:
                    json_data = json.loads(groq_resp[open_brace_index:close_brace_index + 1])

                    string_json_from_llm[ind] = json_data
                    print(f'LLM fixed it!')
                except Exception as mostInnerE:
                    print(f"LLM Couldn't fix the json: {mostInnerE}")
    except Exception as e:
        print(f"Total failure on conversion from string to json of llm output: {e}")


    # Extracting the data from the json_data
    try:
        create_python_objects_from_json_data()
    except Exception as e:
        print(f"Error in Extracting the data from the json_data: {e}")

    # Mapping the method called with method declared
    try:
        mapp_the_function_called_with_method_declared()
    except Exception as e:
        print(f"Error in Mapping the method called with method declared: {e}")

    # Generating the json files for file, class, models, methods, methods called
    try:
        generate_mapped_jsons()
    except Exception as e:
        print(f"Error in Generating the json files for file, class, models, methods, methods called: {e}")

    # Loading data from model folder
    try:
        read_json_and_classify_data_from_model_folder()
    except Exception as e:
        print(f"Error in Loading data from model folder: {e}")

    # Generating json for mermaid
    try:
        generate_json_for_mermaid(url)
    except Exception as e:
        print(f"Error in Generating json for mermaid: {e}")

    # Gerating node representation using mermaid library
    try:
        generate_mermaid()
    except Exception as e:
        print(f"Error in Gerating node representation using mermaid library: {e}")

    return "Success"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_time = time.time()
        print(f"Start time: {start_time}")
        arg = sys.argv[1]
        print(sys.argv)
        print(arg)
        result = read_directory(arg)
        print(result)
        end_time = time.time()

        print(f"Start time: {end_time}")
        print(f"Time Taken: {end_time - start_time}")
    else:
        print("No URL provided")