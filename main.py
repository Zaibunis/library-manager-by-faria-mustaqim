import json
import streamlit as st

LIBRARY_FILE = "library.json"

def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read):
    book_image = f"https://source.unsplash.com/featured/?{title.replace(' ', '%20')},book"
    library.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read, "Image": book_image})
    library.append({"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read})
    save_library(library)

def remove_book(library, title):
    library[:] = [book for book in library if book["Title"].lower() != title.lower()]
    save_library(library)

def search_books(library, keyword):
    return [book for book in library if keyword.lower() in book["Title"].lower() or keyword.lower() in book["Author"].lower()]

def get_statistics(library):
    total = len(library)
    read = sum(1 for book in library if book["Read"])
    return total, (read / total * 100) if total > 0 else 0

def main():
    st.set_page_config(page_title="📖 My Library", page_icon="📚")
    st.title("📚 Personal Library Manager")
    
    # Add custom CSS for the background image
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://source.unsplash.com/featured/?books');
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        </style>
        """, unsafe_allow_html=True
    )
    
    st.markdown("### Welcome to your digital bookshelf! 📖✨")
    st.markdown("Keep track of your favorite books, manage your collection, and explore your reading journey.")
    
    menu = ["🏠 Home", "📖 Add Book", "🗑 Remove Book", "🔍 Search", "📚 Show All", "📊 Statistics"]
    choice = st.sidebar.selectbox("📌 Menu", menu)
    library = load_library()
    
    if choice == "🏠 Home":
        st.image("images/lib.jpg", use_container_width=True)
    
    elif choice == "📖 Add Book":
        st.subheader("📖 Add a New Book")
        title = st.text_input("Title")
        author = st.text_input("Author")
        year = st.number_input("Year", min_value=0, step=1)
        genre = st.text_input("Genre")
        read = st.checkbox("Mark as Read")
        if st.button("➕ Add Book"):
            add_book(library, title, author, year, genre, read)
            st.success("📖 Book added!")
            st.image(f"https://source.unsplash.com/featured/?{title.replace(' ', '%20')},book", use_container_width=True)
    
    elif choice == "🗑 Remove Book":
        st.subheader("🗑 Remove a Book")
        title = st.text_input("Enter title to remove")
        if st.button("❌ Remove"):
            remove_book(library, title)
            st.success("Book removed!")
    
    elif choice == "🔍 Search":
        st.subheader("🔍 Search Books")
        keyword = st.text_input("Enter title or author")
        if st.button("🔎 Search"):
            results = search_books(library, keyword)
            if results:
                for book in results:
                    st.write(f"**📖 {book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")
            else:
                st.warning("No books found!")
    
    elif choice == "📚 Show All":
        st.subheader("📚 Library Collection")
        if library:
            for book in library:
                st.write(f"**📖 {book['Title']}** by {book['Author']} ({book['Year']}) - {book['Genre']} - {'✅ Read' if book['Read'] else '❌ Unread'}")
        else:
            st.info("Your library is empty! 📭")
    
    elif choice == "📊 Statistics":
        st.subheader("📊 Library Stats")
        total, read_pct = get_statistics(library)
        st.write(f"📚 **Total Books:** {total}")
        st.write(f"📖 **Read:** {read_pct:.2f}%")
        st.progress(read_pct / 100)

if __name__ == "__main__":
    main()
