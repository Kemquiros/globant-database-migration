from sqlalchemy import insert
from typing import List
from models.employee import EmployeeModel
from schemes.employee import Employee


class EmployeeService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def get_employees(self):
        result = self.db.query(EmployeeModel).all()
        return result

    def get_employee_by_id(self, id: int):
        result = self.db.query(EmployeeModel).filter(
            EmployeeModel.id == id).first()
        return result

    def create_employee(self, employee: Employee):
        new_employee = EmployeeModel(**employee.dict())
        self.db.add(new_employee)
        self.db.commit()
        return new_employee

    def create_employees(self, employees: List[Employee]):
        try:
            result = self.db.execute(
                insert(EmployeeModel),
                employees
            )
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            with self.db.no_autoflush:
                for employee in employees:
                    employee.employee = employee.employee.strip()
                    new_employee = EmployeeModel(**employee.dict())
                    self.db.merge(new_employee)
                self.db.commit()
            return e

    def update_employee(self, employee_id: int, employee: Employee):
        try:
            updating_employee = self.db.query(EmployeeModel).filter(
                EmployeeModel.id == employee_id).first()
            if not updating_employee:
                return None, None
            updating_employee.id = employee.id
            updating_employee.name = employee.name
            updating_employee.datetime = employee.datetime
            updating_employee.department_id = employee.department_id
            updating_employee.job_id = employee.job_id
            self.db.commit()
            return updating_employee, None
        except Exception as e:
            return None, e

    def delete_employee(self, employee: Employee):
        self.db.delete(employee)
        self.db.commit()
