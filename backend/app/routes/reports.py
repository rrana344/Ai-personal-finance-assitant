import csv
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.demo import DEMO_USER_ID
from app.services.analytics import user_transactions

router = APIRouter(prefix="/reports", tags=["Reports"])
REPORT_DIR = Path("reports")


@router.get("/monthly.csv")
def monthly_csv(db: Session = Depends(get_db)):
    REPORT_DIR.mkdir(exist_ok=True)
    path = REPORT_DIR / "demo-transactions.csv"
    transactions = user_transactions(db, DEMO_USER_ID)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "category", "type", "amount", "payment_method", "status", "notes"])
        for txn in transactions:
            writer.writerow([txn.date, txn.category, txn.type, txn.amount, txn.payment_method, txn.status, txn.notes or ""])
    return FileResponse(path, media_type="text/csv", filename="finmate-report.csv")


@router.get("/monthly.xlsx")
def monthly_excel(db: Session = Depends(get_db)):
    transactions = user_transactions(db, DEMO_USER_ID)
    rows = "".join(
        f"<tr><td>{txn.date}</td><td>{txn.category}</td><td>{txn.type}</td><td>{txn.amount}</td><td>{txn.payment_method}</td><td>{txn.status}</td></tr>"
        for txn in transactions
    )
    excel_rows = (
        rows.replace("<tr>", "<Row>")
        .replace("</tr>", "</Row>")
        .replace("<td>", '<Cell><Data ss:Type="String">')
        .replace("</td>", "</Data></Cell>")
    )
    workbook = f"""<?xml version="1.0"?>
<?mso-application progid="Excel.Sheet"?>
<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet" xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet">
<Worksheet ss:Name="Monthly Report"><Table>
<Row><Cell><Data ss:Type="String">Date</Data></Cell><Cell><Data ss:Type="String">Category</Data></Cell><Cell><Data ss:Type="String">Type</Data></Cell><Cell><Data ss:Type="String">Amount</Data></Cell><Cell><Data ss:Type="String">Payment Method</Data></Cell><Cell><Data ss:Type="String">Status</Data></Cell></Row>
{excel_rows}
</Table></Worksheet></Workbook>"""
    return Response(
        workbook,
        media_type="application/vnd.ms-excel",
        headers={"Content-Disposition": "attachment; filename=finmate-report.xls"},
    )


@router.get("/monthly.pdf")
def monthly_pdf(db: Session = Depends(get_db)):
    transactions = user_transactions(db, DEMO_USER_ID)
    total_income = sum(txn.amount for txn in transactions if txn.type == "income")
    total_expense = sum(txn.amount for txn in transactions if txn.type == "expense")
    body = f"FinMate AI Monthly Report\nIncome: Rs.{total_income:,.0f}\nExpenses: Rs.{total_expense:,.0f}\nSavings: Rs.{total_income - total_expense:,.0f}\nTransactions: {len(transactions)}"
    pdf = _simple_pdf(body)
    return Response(pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=finmate-report.pdf"})


def _simple_pdf(text: str) -> bytes:
    lines = text.splitlines()
    content = "BT /F1 14 Tf 72 760 Td " + " T* ".join(f"({line})" for line in lines) + " ET"
    stream = content.encode("latin-1", errors="replace")
    objects = [
        b"1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj",
        b"2 0 obj << /Type /Pages /Kids [3 0 R] /Count 1 >> endobj",
        b"3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >> endobj",
        b"4 0 obj << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> endobj",
        b"5 0 obj << /Length " + str(len(stream)).encode() + b" >> stream\n" + stream + b"\nendstream endobj",
    ]
    pdf = b"%PDF-1.4\n"
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf += obj + b"\n"
    xref = len(pdf)
    pdf += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode()
    pdf += b"".join(f"{offset:010d} 00000 n \n".encode() for offset in offsets[1:])
    pdf += f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
    return pdf
