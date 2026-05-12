import pandas as pd
from pathlib import Path
from langchain_core.documents import Document


def dataconverter():
    csv_path = Path(__file__).resolve().parents[1] / "data" / "flipkart_product_review.csv"
    product_data = pd.read_csv(csv_path)

    data = product_data[["product_title", "review"]]
    docs = []

    for _, row in data.iterrows():
        doc = Document(
            page_content=str(row["review"]),
            metadata={"product_name": row["product_title"]},
        )
        docs.append(doc)

    return docs




