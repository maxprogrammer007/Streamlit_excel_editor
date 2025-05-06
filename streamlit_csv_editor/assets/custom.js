// assets/custom.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("🌟 Modern Custom JS Loaded");

    const highlightColor = "#2dd4bf";  // Teal glow
    const fadeColor = "#1f2937";       // Dark gray fallback

    // Function to clear all highlights
    const clearAllHighlights = () => {
        document.querySelectorAll(".ag-cell").forEach(cell => {
            cell.style.transition = "background-color 0.3s ease";
            cell.style.backgroundColor = "transparent";
        });
    };

    // Highlight a cell when clicked
    document.querySelectorAll(".ag-cell").forEach(cell => {
        cell.addEventListener("click", () => {
            clearAllHighlights();
            cell.style.backgroundColor = highlightColor;
        });
        cell.addEventListener("mouseover", () => {
            cell.style.cursor = "pointer";
        });
    });

    // Animate rows on mount
    const rows = document.querySelectorAll(".ag-row");
    rows.forEach((row, idx) => {
        row.style.opacity = "0";
        row.style.transform = "translateY(10px)";
        row.style.transition = `opacity 0.5s ${idx * 30}ms ease-out, transform 0.5s ${idx * 30}ms ease-out`;
        setTimeout(() => {
            row.style.opacity = "1";
            row.style.transform = "translateY(0)";
        }, 100);
    });

    // Tooltip for column headers
    document.querySelectorAll(".ag-header-cell-label").forEach(label => {
        const text = label.innerText;
        if (text) {
            label.setAttribute("title", `Column: ${text}`);
        }
    });

    // Smooth scroll into view after load
    const grid = document.querySelector(".ag-root-wrapper");
    if (grid) {
        setTimeout(() => {
            grid.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 300);
    }

    // Add ripple effect to cells
    document.querySelectorAll(".ag-cell").forEach(cell => {
        cell.addEventListener("mousedown", (e) => {
            const ripple = document.createElement("span");
            ripple.className = "ripple";
            ripple.style.left = `${e.offsetX}px`;
            ripple.style.top = `${e.offsetY}px`;
            cell.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
});
