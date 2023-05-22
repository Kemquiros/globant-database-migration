from sqlalchemy import insert
from typing import List
from models.department import DepartmentModel
from schemes.department import Department


class DepartmentService():

    def __init__(self, db) -> None:
        # Bind the database session to the instance
        self.db = db

    def get_departments(self):
        result = self.db.query(DepartmentModel).all()
        return result

    def get_department_by_id(self, id: int):
        result = self.db.query(DepartmentModel).filter(
            DepartmentModel.id == id).first()
        return result

    def create_department(self, department: Department):
        new_department = DepartmentModel(**department.dict())
        self.db.add(new_department)
        self.db.commit()
        return new_department

    def create_departments(self, departments: List[Department]):
        try:
            result = self.db.execute(
                insert(DepartmentModel),
                departments
            )
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            with self.db.no_autoflush:
                for department in departments:
                    department.department = department.department.strip()
                    new_department = DepartmentModel(**department.dict())
                    self.db.merge(new_department)
                self.db.commit()
            return e

    def update_department(self, department_id: int, department: Department):
        updating_department = self.db.query(DepartmentModel).filter(
            DepartmentModel.id == department_id).first()
        if not updating_department:
            return None
        updating_department.id = department.id
        updating_department.department = department.department
        self.db.commit()
        return updating_department

    def delete_department(self, department: Department):
        self.db.delete(department)
        self.db.commit()
