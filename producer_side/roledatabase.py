from flask_webservices.endtoend.producer_side.models import Role  # tables will be created
from flask_webservices.endtoend.producer_side.dbconfig import db

class RoleDatabaseOps:

    def insert_new_role(self,role):
        if role and type(role)==Role:
            drole1 = Role.query.filter(Role.role==role.role).first()
            drole2 = Role.query.filter(Role.code == role.code).first()
            if drole1 or drole2:
                return "Duplicate Role or RoleCode"
            db.session.add(role)
            db.session.commit()
            return True
        return "Invalid Role info"
                            #101-->         ->g102      # SRS -->
    def update_new_role(self,rid,roleinfo): #logically--?       101     admin   a101        102 guest   g101
        if type(roleinfo)==dict:
            if rid and type(rid)==int and rid>0:
                roleinstance = self.fetch_role(rid) #db -->
                if roleinstance:
                    name = roleinfo.get('name')    # name -->self--> sodun baki konakdech nkoy
                    code = roleinfo.get('code')    #code--name -->self--> sodun baki konakdech nkoy
                    rname = Role.query.filter(Role.role==name).first()  # when ?? --> present - [self or other]
                    if rname and rname.id !=roleinstance.id:
                        return "Duplicate Role Name -- this role name is already given to {}".format(rname.id)
                    rcode = Role.query.filter(Role.code == code).first()  # when ?? --> present - [self or other]
                    if rcode and rcode.id != roleinstance.id:
                        return "Duplicate Role Code -- this role code is already given to {}".format(rcode.id)
                    roleinstance.role = name
                    roleinstance.code = code
                    db.session.commit()
                    return True
                else:
                    return "Cannot update as given id record not present"
            else:
                return "Invalid Role Id"
        else:
            return "Incorrect parameters"

    def fetch_role(self,rid):
        if rid and rid>0:
            return Role.query.filter(Role.id==rid,Role.active=='Y').first()

    def fetch_all_roles(self):
        return Role.query.filter(Role.active=='Y').all()

    def remove_role(self,rid):
        returnval = None
        if rid and type(rid)==int and rid>0:
            roleinstance = self.fetch_role(rid)
            if roleinstance:
                #db.session.delete(roleinstance)
                roleinstance.active='N'
                db.session.commit()
                returnval=True  #exit
            else:
                returnval="Role Id not present cannot be removed"   #exit
        else:
            returnval="Invalid Role Id" #exit

        return returnval        # exit point is here