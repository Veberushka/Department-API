        
def build_Tree_with_recursion(all_department:list[dict],id:int,depth:int)->list[dict]:


    current_departament= next((i for i in all_department if i['id'] == id), None)
    if not current_departament:
        return None
    if depth > 1:
        children=[]
        for department in all_department:
            if department['parent_id']==id:
                child_tree=build_Tree_with_recursion(all_department,department['id'],depth-1)
                children.append(child_tree)
        current_departament['children']=children
    else:
        current_departament['children']=[]
    return current_departament


def sort_Tree(department:dict,sort_by:str)->dict:


    if department['employees']:
        department['employees'].sort(key=lambda x: x[sort_by])
        for child in department['children']:
            sort_Tree(child,sort_by)
    return department

def collect_department_ids(department_tree:dict,departmen_id:int,depth=5,exception=None)->list[int]:
    if exception==None:
        exception=[]
    exception.append(departmen_id)  
    if depth > 1 and 'children' in department_tree:
       for child in department_tree.get('children', []):
            collect_department_ids(child, child['id'], depth - 1, exception)
    return exception

def collect_department_names(department_tree:dict,departmen_id:int,departament_name:str|None=None,depth=2,exception=None)->list[int]:
    if exception==None:
        exception=[]
    if departament_name:
        exception.append(departament_name)  
    if depth > 1 and 'children' in department_tree:
       for child in department_tree.get('children', []):
            collect_department_names(child, child['id'],child['name'], depth - 1, exception)
    return exception                

    
