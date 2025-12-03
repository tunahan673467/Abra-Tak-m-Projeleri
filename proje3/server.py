import json
import os
import zmq

DB_FILE = "ornek.json"


def load_db():
    if not os.path.exists(DB_FILE):
        return {"books": []}

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def find_next_id(books):
    if not books:
        return 1
    return max(book["id"] for book in books) + 1


def handle_search(db, query):
    books = db.get("books", [])
    q = query.lower()
    results = [
        book
        for book in books
        if q in book["title"].lower() or q in book["author"].lower()
    ]

    return {
        "status": "success",
        "message": f"{len(results)} sonuç bulundu.",
        "results": results
    }


def handle_add(db, book_data):
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in book_data:
            return {"status": "error", "message": f"Eksik alan: {field}"}

    books = db["books"]
    new_book = {
        "id": find_next_id(books),
        "title": book_data["title"],
        "author": book_data["author"],
        "year": book_data["year"],
        "available": True,
        "borrowed_by": None,
    }

    books.append(new_book)
    save_db(db)

    return {"status": "success", "message": "Kitap eklendi.", "book": new_book}


def handle_borrow(db, book_id, user):
    books = db["books"]

    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                return {"status": "error", "message": "Kitap zaten ödünç verilmiş."}

            book["available"] = False
            book["borrowed_by"] = user
            save_db(db)

            return {
                "status": "success",
                "message": f"{book['title']} ödünç alındı.",
                "book": book
            }

    return {"status": "error", "message": "Kitap bulunamadı."}


def handle_return(db, book_id):
    """Kitap iade eder."""
    books = db["books"]

    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                return {"status": "error", "message": "Kitap zaten kütüphanede."}

            book["available"] = True
            book["borrowed_by"] = None
            save_db(db)

            return {
                "status": "success",
                "message": f"{book['title']} başarıyla iade edildi.",
                "book": book
            }

    return {"status": "error", "message": "Kitap bulunamadı."}


def handle_request(request_json):
    db = load_db()
    action = request_json.get("action")

    if action == "search":
        return handle_search(db, request_json.get("query", ""))

    elif action == "add":
        return handle_add(db, request_json.get("book", {}))

    elif action == "borrow":
        book_id = request_json.get("id")
        user = request_json.get("user")
        return handle_borrow(db, book_id, user)

    elif action == "return":
        book_id = request_json.get("id")
        return handle_return(db, book_id)

    else:
        return {"status": "error", "message": "Bilinmeyen action."}


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Sunucu başlatıldı... (ZeroMQ REP)")

    while True:
        try:
            message = socket.recv_string()
            print("İstek:", message)

            try:
                req_json = json.loads(message)
            except:
                response = {"status": "error", "message": "Geçersiz JSON"}
            else:
                response = handle_request(req_json)

            socket.send_string(json.dumps(response, ensure_ascii=False))

        except KeyboardInterrupt:
            print("Sunucu kapatılıyor...")
            break

    socket.close()
    context.term()


if __name__ == "__main__":
    main()
