import pandas as pd
from dotenv import load_dotenv
from langgraph.constants import Send
from langchain_community.vectorstores.faiss import FAISS
from pydantic import BaseModel ,AnyUrl
from langchain_core.tools import ToolException
from langchain.tools import tool
from langchain_core.vectorstores import VectorStoreRetriever

from langchain_voyageai import VoyageAIEmbeddings
from pydantic import Field

load_dotenv()

embeddings = VoyageAIEmbeddings(
    model="voyage-2", batch_size=128, truncation=True
)


class Loan_input(BaseModel):
    name: str = Field(description="The name of the customer")
    rate: int = Field(description="rate at which loan amount will be calculated")


@tool("loan_tool", args_schema=Loan_input)
def monthly_payment(name: str, rate: int) -> str:
    """
            This tool will help to give new monthly payment for user
            :param rate:  rate at which loan amount will be calculated
            :param name:  name of the customer
            :return: string the amount the customer will pay this month
            """
    try:
        df = pd.read_csv("Loan_amount.csv")
        df.set_index('Name', inplace=True)
        interest_rate = rate / 100  #
        monthly_payment = df.loc[name]['Monthly_Payment']
        new_monthly_payment = monthly_payment * (1 - interest_rate)
        df.reset_index(inplace=True)
        if rate == 10:
            return f"This will be the last {new_monthly_payment}  payment for the customer {name}"
        elif rate == 5:
            return f"The initial discounted loan amount will be {new_monthly_payment} for the customer {name}"
    except Exception as e:
        raise ToolException("The search tool1 is not available.", e)


def monthly_payment_1(name: str, rate: int) -> str:
    """
            This tool will help to give new monthly payment for user
            :param rate:  rate at which loan amount will be calculated
            :param name:  name of the customer
            :return: string the amount the customer will pay this month
            """
    try:
        df = pd.read_csv("Loan_amount.csv")
        df.set_index('Name', inplace=True)
        interest_rate = rate / 100  #
        monthly_payment = df.loc[name]['Monthly_Payment']
        new_monthly_payment = monthly_payment * (1 - interest_rate)
        df.reset_index(inplace=True)
        if rate == 10:
            return f"This will be the last {new_monthly_payment}  payment for the customer {name}"
        elif rate == 5:
            return f"The initial discounted loan amount will be {new_monthly_payment} for the customer {name}"
    except Exception as e:
        raise ToolException("The search tool1 is not available.", e)


def loan_embedding_model() -> VectorStoreRetriever:
    new_db = FAISS.load_local("faiss_index_loan_voyage1", embeddings, allow_dangerous_deserialization=True)
    new_db = new_db.as_retriever(search_kwargs={"k": 1})
    return new_db


#doc=loan_embedding_model().get_relevant_documents("james")
#print(doc)