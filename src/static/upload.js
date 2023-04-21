function uploadFiles() {
    const input = document.getElementById("folder-input");
    const files = input.files;
    const status = document.getElementById("status");

    if (files.length === 0) {
        status.innerHTML = "No files selected";
        return;
    }

    // Add this line to display the message before processing the files
    status.innerHTML = "Thanks, I will process your files";

    const formData = new FormData();

    for (let i = 0; i < files.length; i++) {
        formData.append("file" + i, files[i]);
    }

    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            if (response.ok) {
                status.innerHTML = "Files uploaded successfully";
                // Add this line to redirect the user after a successful file upload
                window.location.href = "/dashapp/";
            } else {
                status.innerHTML = "Error uploading files";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            status.innerHTML = "Error uploading files";
        });
}
