from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List

import enum

db = SQLAlchemy()

class state_type(enum.Enum):
    APPROVED= 'approved'
    DENEGATED= 'denegated'
    PENDING= 'pending'


class Employee(db.Model):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    last_name: Mapped[str] =mapped_column(String(250), nullable=False)
    email: Mapped[str]= mapped_column(String(120), unique=True, nullable=False)
    supervisor: Mapped[bool]=mapped_column(String(250), nullable=False)
    departament_id: Mapped[int] = mapped_column(ForeignKey('departments.id'), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # departamentos: Mapped['Departamento'] = relationship(
    #     back_populates="empleado"
    # )

    # presupuestos: Mapped[List['Presupuesto']] = relationship(
    #     back_populates="empleado"
    # )




class Department(db.Model):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    # presupuestos: Mapped['Presupuesto'] = relationship(
    #     back_populates="departamento"
    # )



class Bill(db.Model):
    __tablename__ = "bills"

    id: Mapped[int] = mapped_column(primary_key=True)
    trip_description: Mapped[str] = mapped_column(String(250), nullable=False)
    trip_address: Mapped[str] =mapped_column(String(250), nullable=False)
    state: Mapped[state_type]= mapped_column(Enum(state_type))
    amount: Mapped[str]=mapped_column(String(250), nullable=False)
    evaluator_id: Mapped[int]= mapped_column(ForeignKey('employees.id'), nullable=False)
    date_approved: Mapped[datetime] = mapped_column(Boolean(), nullable=False)
    budget_id: Mapped[int]= mapped_column(ForeignKey('budgets.id'), nullable=False)

    # presupuestos: Mapped['Presupuesto'] = relationship(
    #     back_populates="Factura"
    # )


class Budget(db.Model):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    budget_description: Mapped[str] = mapped_column(String(250), nullable=False)
    employee_id: Mapped[int]= mapped_column(ForeignKey('employees.id'), nullable=False)
    department_id: Mapped[int]= mapped_column(ForeignKey('departments.id'), nullable=False)
