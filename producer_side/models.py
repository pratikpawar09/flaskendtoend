from flask_webservices.endtoend.producer_side.dbconfig import db
import datetime

                                #relationship
# employee --> user               emp_role --> many to many
# role                            emp_address--> one to many  address_emp --> many to one
# Address                         emp_login --> one to one
# login

#employee              address         role        login            emp_role
#   eid                aid eid                     lid eid           eid rid

emp_role = db.Table("emp_role",
                    db.Column("eid",db.ForeignKey("employee.id"),primary_key=True),
                    db.Column("rid",db.ForeignKey("role.id"),primary_key=True),
                    db.Column('created',db.DateTime, server_default=db.func.now()),
                    db.Column('active',db.String(50),default="Y")
            )

class Employee(db.Model):   # service and ui --> for emp--> emp -- multiple addresses-->
    id = db.Column("id",db.Integer(),primary_key=True)
    name = db.Column("emp_name",db.String(50))
    salary = db.Column("emp_salary",db.Float())
    joining = db.Column('travel_date',db.DateTime,default = datetime.datetime.now())
    photo = db.Column('photo_url',db.String(50),default="NA")
    active = db.Column('active',db.String(50),default="Y")
    created = db.Column('created',db.DateTime, server_default=db.func.now())
    updated = db.Column('modified',db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    adrrefs = db.relationship("Address",backref="empref",uselist=True,lazy=True)
    loginref = db.relationship("Login",backref="empref",uselist=False,lazy=True)

class Address(db.Model):    # i am not going to write service for this....>
    id =  db.Column("id", db.Integer(),primary_key=True)
    city = db.Column("city", db.String(50))
    state = db.Column("state", db.String(50))
    pincode = db.Column("pincode", db.Integer())
    active = db.Column('active',db.String(50),default="Y")
    created = db.Column('created',db.DateTime, server_default=db.func.now())
    updated = db.Column('modified',db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    empid = db.Column("emp_id",db.ForeignKey("employee.id"),unique=False,null=True)       #FK --??

class Role(db.Model):
    id =  db.Column("id", db.Integer(),primary_key=True)
    role = db.Column("role", db.String(50),unique=True,nullable=False)
    code = db.Column("code", db.String(50),unique=True,nullable=False)
    emprefs = db.relationship(Employee,secondary = emp_role,backref=db.backref("roleref",lazy=True))
    active = db.Column('active', db.String(50), default="Y")
    created = db.Column('created', db.DateTime, server_default=db.func.now())
    updated = db.Column('modified', db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

#Role(role,code)

class Login(db.Model):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column("username", db.String(50),unique=True,nullable=False)
    password = db.Column("password", db.String(50),nullable=False)
    empid = db.Column("emp_id",db.ForeignKey("employee.id"),unique=True)


db.create_all()  # whoever imports to this module--> db tables shud be created..

if __name__ == '__main__':
    db.create_all()