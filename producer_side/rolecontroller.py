from flask_webservices.endtoend.producer_side.dbconfig import db,app
from flask_webservices.endtoend.producer_side.models import Role
import json
from flask import request
from flask_webservices.endtoend.producer_side.roledatabase import RoleDatabaseOps

#role crud operations -->
BASE_ROUTE = "/app/role/"       #http://localhost:5000/app/role/

roledb = RoleDatabaseOps()  # can access to instance methods-->

def check_for_role_input(roleinfo):
    errors ={}
    if roleinfo:
        if not roleinfo.get('rname'):
            errors['rname'] = "Required Role Name"
        if not roleinfo.get('rcode'):
            errors['rcode'] = "Required Role code"
        return errors

    errors['fields'] = "Rolename and RoleCode Required"
    return errors

@app.route(BASE_ROUTE,methods = ["POST"])   #http://localhost:5000/app/role/    --> post
def add_new_role(): #app
    roleinfo = request.get_json()
    print('RoleInfo -->',roleinfo)

    errors = check_for_role_input(roleinfo)
    if errors:
        return json.dumps(errors)
    else:
        rl = Role(role=roleinfo.get('rname'),code=roleinfo.get('rcode'))
        msg = roledb.insert_new_role(rl)
        if msg==True:
            return json.dumps({"status" : "Role Record Inserted"})
        else:
            return json.dumps({"error":msg})



@app.route(BASE_ROUTE+"<int:rid>",methods = ["PUT"])        # http://localhost:5000/app/role/{id}    --> type
def update_role_info(rid):
    roleinfo = request.get_json()
    errors = check_for_role_input(roleinfo)
    if errors:
        return json.dumps(errors)
    else:
        msg = roledb.update_new_role(rid,{"name":roleinfo.get("rname"),"code":roleinfo.get("rcode")})
        if msg==True:
            return json.dumps({"status" : "Role Record Updated..."})
        else:
            return json.dumps({"error" : msg})

def serialize_data(instance):
    return {"name":instance.role,"code":instance.code,"id":instance.id}

@app.route(BASE_ROUTE+"<int:rid>",methods = ["DELETE"])
def delete_role(rid):
    msg = roledb.remove_role(rid)
    if msg ==True:
        return json.dumps({"status" :"Record Removed..!"})
    else:
        return json.dumps({"error" : msg})

@app.route(BASE_ROUTE+"<int:rid>",methods = ["GET"])
def get_single_role(rid):
    roleinstance = roledb.fetch_role(rid)
    if roleinstance:
        return json.dumps(serialize_data(roleinstance))
    else:
        return json.dumps({"error": "No record present with Given Id"})


@app.route(BASE_ROUTE,methods = ["GET"])
def get_all_roles():
    roles = roledb.fetch_all_roles()
    if roles:
        listOfRoles = []
        for role in roles:
            listOfRoles.append(serialize_data(role))
        return json.dumps(listOfRoles)
    return json.dumps({"error" : "No records...!"})

@app.route(BASE_ROUTE+"by/",methods=["POST"])    #http://localhost:5000/app/role/by/     -->search criteria
def search_by():
    roleinfo = request.get_json()
    name = roleinfo.get("rname")
    flag = False
    if name:
        flag=True
        roleinstance = Role.query.filter(Role.role==name).first()
        if roleinstance:
            return json.dumps(serialize_data(roleinstance))
    code = roleinfo.get("rcode")
    if code:
        flag = True
        roleinstance = Role.query.filter(Role.code==code).first()
        if roleinstance:
            return json.dumps(serialize_data(roleinstance))

    if flag:
        return json.dumps({"error" : "No records found with given Params"})
    return json.dumps({"error" : "Search params required..!"})




if __name__ == '__main__':
    app.run(debug=True)