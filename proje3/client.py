import json
import zmq


def print_response(resp):
    status = resp.get("status")
    message = resp.get("message", "")
    print(f"\n[Durum] {status}")
    print(f"[Mesaj] {message}")

    if "book" in resp:
        book = resp["book"]
        print(
            f"Kitap: ID={book['id']}, {book['title']} "
            f"({book['author']}, {book['year']}), "
            f"Müsait: {'Evet' if book['available'] else 'Hayır'} "
        )

    if "results" in resp:
        print("\n[Arama Sonuçları]")
        for b in resp["results"]:
            print(
                f"- ID={b['id']}, {b['title']} ({b['author']}), "
                f"Müsait: {'Evet' if b['available'] else 'Hayır'}"
            )


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    print("İstemci başlatıldı. (ZeroMQ REQ)")

    while True:
        print("\n--- KÜTÜPHANE MENÜ ---")
        print("1) Kitap ara")
        print("2) Kitap ekle")
        print("3) Kitap ödünç al")
        print("4) Kitap iade et")
        print("5) Çıkış")

        secim = input("Seçiminiz: ").strip()

        if secim == "1":
            query = input("Aranacak kelime: ")
            req = {"action": "search", "query": query}

        elif secim == "2":
            title = input("Başlık: ")
            author = input("Yazar: ")
            year = int(input("Yıl: "))
            req = {
                "action": "add",
                "book": {"title": title, "author": author, "year": year},
            }

        elif secim == "3":
            book_id = int(input("Ödünç alınacak kitap ID: "))
            user = input("Kullanıcı adı: ")
            req = {"action": "borrow", "id": book_id, "user": user}

        elif secim == "4":
            book_id = int(input("İade edilecek kitap ID: "))
            req = {"action": "return", "id": book_id}

        elif secim == "5":
            print("İstemci kapatılıyor...")
            break

        else:
            print("Geçersiz seçim!")
            continue

        socket.send_string(json.dumps(req, ensure_ascii=False))
        response = socket.recv_string()
        print_response(json.loads(response))

    socket.close()
    context.term()


if __name__ == "__main__":
    main()
