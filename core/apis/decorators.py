import json
import pdb
from flask import request
from core.libs import assertions
from functools import wraps
from core.models.teachers import Teacher
from core.models.students import Student
from core.models.principals import Principal
from core.models.users import User

class AuthPrincipal:
    def __init__(self, user_id, student_id=None, teacher_id=None, principal_id=None):
        self.user_id = user_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.principal_id = principal_id


def accept_payload(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        incoming_payload = request.json
        return func(incoming_payload, *args, **kwargs)
    return wrapper


def authenticate_principal(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        p_str = request.headers.get('X-Principal')
        assertions.assert_auth(p_str is not None, 'principal not found')
        p_dict = json.loads(p_str)
        p = AuthPrincipal(
            user_id=p_dict['user_id'],
            student_id=p_dict.get('student_id'),
            teacher_id=p_dict.get('teacher_id'),
            principal_id=p_dict.get('principal_id')
        )
        user = User.get_by_id(p.user_id)
        if user is None: 
            raise ValueError("User not found")

        if request.path.startswith('/student'):
            student = Student.get_by_id(p.student_id)
            if student[0].user_id != p.user_id:
                raise ValueError("requester should be a student")
            assertions.assert_true(p.student_id is not None, 'requester should be a student')
        elif request.path.startswith('/teacher'):
            teacher = Teacher.get_by_id(p.teacher_id)
            if teacher[0].user_id != p.user_id:
                raise ValueError("requester should be a teacher")
            assertions.assert_true(p.teacher_id is not None, 'requester should be a teacher')
        elif request.path.startswith('/principal'):
            principal = Principal.get_by_id(p.principal_id)
            if principal[0].user_id != p.user_id:
                raise ValueError("requester should be a principal")
            assertions.assert_true(p.principal_id is not None, 'requester should be a principal')
        else:
            assertions.assert_found(None, 'No such api')

        return func(p, *args, **kwargs)
    return wrapper
