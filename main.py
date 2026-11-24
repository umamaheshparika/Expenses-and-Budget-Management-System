from fastapi import FastAPI,Request,Form,Depends,status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from sqlalchemy import create_engine,Column,Integer,String,Boolean,Float,DateTime,func,ForeignKey
from datetime import datetime
from sqlalchemy.orm import declarative_base,sessionmaker,Session,relationship
app = FastAPI()

templates = Jinja2Templates(directory="templates")


class verification(BaseModel):
    expenses_name : str
    amount : float
    payment_method : str
    description : str

 
DATABASE_URL = "sqlite:///./financial.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={'check_same_thread':False}
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Financial(Base):
    __tablename__ = "expenses"
    exp_id = Column(Integer,primary_key=True,index=True)
    expenses_name = Column(String,nullable=False)
    amount = Column(Float,nullable=False)
    payment_method = Column(String,nullable=False)
    description = Column(String)
    exp_date = Column(DateTime,default=datetime.now)
    budget_id = Column(Integer,ForeignKey("budget.budget_id"))
    budget = relationship("Budget",back_populates="expenses")

# Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main_home(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="main_home_page.html",
        context={}
    )
@app.get("/exp")
def home(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={}
    )

@app.get("/bud")
def budget_home(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="bud_home.html",
        context={}
    )
@app.get("/exp/add")
def add(req:Request,db:Session = Depends(get_db)):
    all_budgets = db.query(Budget).all()
    return templates.TemplateResponse(
        request=req,
        name="form.html",
        context={
            "budgets":all_budgets
        }
    )

@app.post("/exp/add")
def exp_details(
    expenses_name:str = Form(),
    amount:float = Form(),
    payment_method:str = Form(),
    description:str = Form(),db:Session = Depends(get_db)):
    verify_obj = verification(
        expenses_name=expenses_name,
        amount=amount,
        payment_method=payment_method,
        description=description
    )
    expenses_obj = Financial(
        expenses_name = verify_obj.expenses_name,
        amount = verify_obj.amount,
        payment_method = verify_obj.payment_method,
        description = verify_obj.description
    )
    db.add(expenses_obj)
    db.commit()

    return RedirectResponse(url="/exp",status_code=303)

@app.get("/exp/all")
def all_expensess(req:Request,db:Session = Depends(get_db)):
    all_exps = db.query(Financial).all()
    return templates.TemplateResponse(
        request=req,
        name="view_all.html",
        context={
            "exps":all_exps
        }

    )
@app.get("/exp/update/{exp_id}")
def edit(exp_id, req:Request,db:Session = Depends(get_db) ):
    single_exp = db.query(Financial).filter(
        Financial.exp_id == exp_id
    ).first()
    budgets = db.query(Budget).all()
    return templates.TemplateResponse(
        request=req,
        name="update_form.html",
        context={
            "exp":single_exp,
            "budgets":budgets
        }
    )
@app.post("/exp/update/{exp_id}")
def update(exp_id,
    expenses_name:str = Form(),
    amount:float = Form(),
    payment_method:str = Form(),
    description:str = Form(),db:Session = Depends(get_db)):
    verify_obj = verification(
            expenses_name=expenses_name,
            amount=amount,
            payment_method=payment_method,
            description=description
        )
    single_exp = db.query(Financial).filter(
        Financial.exp_id == exp_id
    ).first()
    single_exp.expenses_name = verify_obj.expenses_name
    single_exp.amount = verify_obj.amount
    single_exp.payment_method = verify_obj.payment_method
    single_exp.description = verify_obj.description
    db.commit()
    return RedirectResponse("/exp/all",status_code=303)
@app.post("/exp/delete/{exp_id}")
def delete(exp_id,db:Session = Depends(get_db)):
    single_exp = db.query(Financial).filter(
        Financial.exp_id == exp_id
    ).first()
    db.delete(single_exp)
    db.commit()
    return RedirectResponse("/exp/all",status_code=303)

@app.get("/exp/by/amount")
def view_by_amount(req:Request,db:Session = Depends(get_db)):
    exps_by_amount = db.query(Financial).order_by(Financial.amount.desc()).all()
    return templates.TemplateResponse(
        request=req,
        name="view_by_amount.html",
        context={
            "exps":exps_by_amount
        }
    )

@app.get("/exp/by/method")
def select_method(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="show_methods.html",
        context={}
    )


@app.get("/exp/by/{method}")
def view_by_method(method: str, req: Request, db: Session = Depends(get_db)):

    view_by_payment = db.query(Financial).filter(
        Financial.payment_method == method
    ).all()

    print(view_by_payment)

    return templates.TemplateResponse(
        request=req,
        name="view_by_method.html",
        context={
            "exps": view_by_payment
        }
    )


@app.get("/exp/month")
def month_wise(req:Request,db:Session = Depends(get_db)):
    month_wise_exps = db.query(func.strftime("%Y-%m",Financial.exp_date).label("month"),func.sum(Financial.amount).label("total")).group_by(func.strftime("%Y-%m",Financial.exp_date)).order_by(func.strftime("%Y-%m",Financial.exp_date)).all()
    return templates.TemplateResponse(
        request=req,
        name="month_wise_exp.html",
        context={
            "exps":month_wise_exps
        }
    )

@app.get("/exp/{month}")
def date_wise_exps(month:str, req:Request, db:Session = Depends(get_db)):
    date_wise = db.query(Financial).filter(
        func.strftime("%Y-%m",Financial.exp_date) == month

    ).all()
    return templates.TemplateResponse(
        request=req,
        name="date_wise_exps.html",
        context={
            "exps":date_wise,
            "month":month
        }
    )

"====================================BUDGET TABLE==========================="
class Budget(Base):
    __tablename__ = "budget"
    budget_id = Column(Integer,primary_key=True,index=True)
    budget_amount = Column(Float,nullable=False)
    month = Column(Integer,nullable=False)
    year = Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.now)
    expenses = relationship("Financial",back_populates="budget")

Base.metadata.create_all(bind=engine)


class check(BaseModel):
    budget_amount:float
    month:int
    year:int

@app.get("/add/budget")
def budget_form(req:Request):
    return templates.TemplateResponse(
        request=req,
        name="budget_form.html",
        context={}
    )
@app.post("/add/budget")
def enter_budget(
    budget_amount:float = Form(),
    month:int = Form(),
    year:int = Form(),
    db:Session = Depends(get_db) ):
    check_obj = check(budget_amount=budget_amount,
          month=month,
          year=year)
    print(check_obj)
    budget_obj = Budget(
        budget_amount = check_obj.budget_amount,
        month = check_obj.month,
        year = check_obj.year
    )
    db.add(budget_obj)
    db.commit()
    return RedirectResponse(url="/bud",status_code=303)
@app.get("/view/budget")
def view_all_budgets(req:Request,db:Session = Depends(get_db)):
    view_all = db.query(Budget).all()
    return templates.TemplateResponse(
        request=req,
        name="view_all_budgets.html",
        context={
            "buds":view_all
        }
    )

@app.get("/budget/edit/{budgt_id}")
def edit_budgt(budgt_id, req:Request,db:Session = Depends(get_db)):
    single_budgt = db.query(Budget).filter(
        Budget.budget_id == budgt_id
        ).first()
    return templates.TemplateResponse(
        request=req,
        name="edit_budgt_form.html",
        context={
            "bud":single_budgt
        }
    )
@app.post("/budget/upadate/{budgt_id}")
def update_budgt(budgt_id,db:Session = Depends(get_db),
                 budget_amount = Form(),
                 month = Form(),
                 year = Form()):
    update_verified_obj = check(
        budget_amount=budget_amount,
        month=month,
        year=year
    )
    # print(update_verified_obj)

    old_budgt_data = db.query(Budget).filter(
        Budget.budget_id == budgt_id
    ).first()
    old_budgt_data.budget_amount = update_verified_obj.budget_amount
    old_budgt_data.month = update_verified_obj.month
    old_budgt_data.year = update_verified_obj.year
    db.commit()
    return RedirectResponse(url="/view/budget",status_code=303)


@app.post("/budget/delete/{budgt_id}")
def delete_budgt(budgt_id:int,db:Session = Depends(get_db)):
    single_budgt = db.query(Budget).filter(
        Budget.budget_id == budgt_id
    ).first()
    db.delete(single_budgt)
    db.commit()
    return RedirectResponse(url="/view/budget",status_code=303)

@app.get("/budget/remaining")
def remaining_budget(req: Request, db: Session = Depends(get_db)):

    budgets = db.query(Budget).all()

    budget_details = []

    for budget in budgets:

        total_expenses = db.query(func.sum(Financial.amount)).filter(
            Financial.budget_id == budget.budget_id
        ).scalar() or 0

        remaining_amount = budget.budget_amount - total_expenses

        budget_details.append({
            "month": budget.month,
            "year": budget.year,
            "budget_amount": budget.budget_amount,
            "total_expenses": total_expenses,
            "remaining_amount": remaining_amount
        })

    return templates.TemplateResponse(
        request=req,
        name="remaining_budget.html",
        context={
            "buds": budget_details
        }
    )




