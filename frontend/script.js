const pdfInput = document.getElementById("pdfInput");
const uploadStatus = document.getElementById("uploadStatus");
const documentCard = document.getElementById("documentCard");
const filename = document.getElementById("filename");
const chunkCount = document.getElementById("chunkCount");

const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");

let documentId = null;
let busy = false;


function addMessage(text, role, sources = []) {
    const welcome = chatMessages.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }

    const bubble = document.createElement("div");
    bubble.className = `message ${role}`;

    // Use textContent to display responses safely.
    bubble.textContent = text;

    if (sources.length > 0) {
        const sourceElement = document.createElement("div");
        sourceElement.className = "sources";
        sourceElement.textContent =
            "Retrieved pages: " + sources.join(", ");

        bubble.appendChild(sourceElement);
    }

    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    return bubble;
}


function setBusy(value) {
    busy = value;
    sendBtn.disabled = value;
    pdfInput.disabled = value;
    newChatBtn.disabled = value;
}


// Upload PDF
pdfInput.addEventListener("change", async () => {
    const file = pdfInput.files[0];

    if (!file || busy) return;

    if (!file.name.toLowerCase().endsWith(".pdf")) {
        uploadStatus.textContent = "Please select a PDF file.";
        pdfInput.value = "";
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setBusy(true);
    documentId = null;
    documentCard.classList.add("hidden");
    uploadStatus.textContent = "Uploading and processing PDF...";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed");
        }

        documentId = data.document_id;

        filename.textContent = data.filename;
        chunkCount.textContent =
            `${data.total_chunks} chunks indexed`;

        documentCard.classList.remove("hidden");

        uploadStatus.textContent = "Document ready for questions.";

        chatMessages.innerHTML = "";

        addMessage(
            `Your document "${data.filename}" is ready. What would you like to know?`,
            "bot"
        );

    } catch (error) {
        uploadStatus.textContent = error.message;

    } finally {
        setBusy(false);
        pdfInput.value = "";
    }
});


// Send question
chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question || busy) return;

    if (!documentId) {
        addMessage("Please upload a PDF first.", "bot");
        return;
    }

    addMessage(question, "user");
    questionInput.value = "";

    const loadingBubble = addMessage("Thinking...", "bot");

    setBusy(true);

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                document_id: documentId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : "Unable to answer the question."
            );
        }

        loadingBubble.remove();

        addMessage(
            data.answer,
            "bot",
            data.sources || []
        );

    } catch (error) {
        loadingBubble.remove();
        addMessage("Error: " + error.message, "bot");

    } finally {
        setBusy(false);
        questionInput.focus();
    }
});


// Press Enter to send, Shift+Enter for a new line
questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();

        chatForm.requestSubmit();
    }
});


// Clear chat, keeping the uploaded PDF selected
newChatBtn.addEventListener("click", () => {
    if (busy) return;

    chatMessages.innerHTML = "";
    questionInput.value = "";

    addMessage(
        documentId
            ? "New conversation started. Ask about your uploaded PDF."
            : "Upload a PDF to begin.",
        "bot"
    );
});