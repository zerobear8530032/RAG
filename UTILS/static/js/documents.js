/**
 * Documents Page JavaScript
 * Handles document management functionality
 */


document.addEventListener('DOMContentLoaded', function() {
    // Document search functionality
    const searchInput = document.getElementById('document-search');
    const searchBtn = document.getElementById('search-btn');
    const documentItems = document.querySelectorAll('.document-item');
    
    function searchDocuments(query) {
        query = query.toLowerCase().trim();
        
        documentItems.forEach(item => {
            const documentName = item.querySelector('h3').textContent.toLowerCase();
            if (documentName.includes(query) || query === '') {
                item.style.display = 'grid';
            } else {
                item.style.display = 'none';
            }
        });
    }
    
    if (searchInput && searchBtn) {
        searchBtn.addEventListener('click', () => {
            searchDocuments(searchInput.value);
        });
        
        searchInput.addEventListener('keyup', (e) => {
            if (e.key === 'Enter') {
                searchDocuments(searchInput.value);
            }
        });
    }
    
    // Document sorting functionality
    const sortSelect = document.getElementById('sort-documents');
    const documentList = document.querySelector('.document-list');
    
    function sortDocuments(criteria) {
        const items = Array.from(documentItems);
        
        items.sort((a, b) => {
            const aName = a.querySelector('h3').textContent;
            const bName = b.querySelector('h3').textContent;
            const aDate = a.querySelector('p').textContent;
            const bDate = b.querySelector('p').textContent;
            const aIsFolder = a.classList.contains('folder');
            const bIsFolder = b.classList.contains('folder');
            
            // Always put folders first
            if (aIsFolder && !bIsFolder) return -1;
            if (!aIsFolder && bIsFolder) return 1;
            
            switch (criteria) {
                case 'name':
                    return aName.localeCompare(bName);
                case 'date':
                    return bDate.localeCompare(aDate); // Most recent first
                case 'type':
                    const aType = aName.split('.').pop();
                    const bType = bName.split('.').pop();
                    return aType.localeCompare(bType);
                default:
                    return 0;
            }
        });
        
        // Remove existing items
        items.forEach(item => item.remove());
        
        // Add sorted items back
        items.forEach(item => documentList.appendChild(item));
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            sortDocuments(sortSelect.value);
        });
    }
    
    // Upload modal functionality
    const uploadBtn = document.getElementById('upload-btn');
    const uploadModal = document.getElementById('upload-modal');
    const closeUploadModal = uploadModal?.querySelector('.close');
    const uploadForm = document.getElementById('upload-form');
    
    if (uploadBtn && uploadModal) {
        uploadBtn.addEventListener('click', () => {
            uploadModal.style.display = 'block';
        });
        
        closeUploadModal.addEventListener('click', () => {
            uploadModal.style.display = 'none';
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === uploadModal) {
                uploadModal.style.display = 'none';
            }
        });
        
            }
    
    // Create folder modal functionality
    const createFolderBtn = document.getElementById('create-folder-btn');
    const folderModal = document.getElementById('folder-modal');
    const closeFolderModal = folderModal?.querySelector('.close');
    const folderForm = document.getElementById('folder-form');
    
    if (createFolderBtn && folderModal) {
        createFolderBtn.addEventListener('click', () => {
            folderModal.style.display = 'block';
        });
        
        closeFolderModal.addEventListener('click', () => {
            folderModal.style.display = 'none';
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === folderModal) {
                folderModal.style.display = 'none';
            }
        });
        
        folderForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            // Get form data
            const folderName = document.getElementById('folder-name').value;
            const parentFolder = document.getElementById('parent-folder').value;
            
            // In a real application, you would create this folder on the server
            // For demo purposes, just show a success message
            alert(`Folder ${folderName} created in ${parentFolder} successfully!`);
            
            // Close the modal
            folderModal.style.display = 'none';
            
            // Reset the form
            folderForm.reset();
        });
    }
    
    // Document action buttons
    const actionBtns = document.querySelectorAll('.document-actions .action-btn');
    
    actionBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const documentItem = btn.closest('.document-item');
            const documentName = documentItem.querySelector('h3').textContent;
            
            // Create a simple dropdown menu
            const dropdown = document.createElement('div');
            dropdown.className = 'action-dropdown';
            dropdown.style.position = 'absolute';
            dropdown.style.right = '10px';
            dropdown.style.top = btn.offsetTop + btn.offsetHeight + 'px';
            dropdown.style.backgroundColor = 'var(--color-bg-primary)';
            dropdown.style.boxShadow = 'var(--box-shadow)';
            dropdown.style.borderRadius = 'var(--border-radius)';
            dropdown.style.zIndex = '10';
            
            const actions = [
                { text: 'Open', icon: 'fa-eye' },
                { text: 'Download', icon: 'fa-download' },
                { text: 'Rename', icon: 'fa-edit' },
                { text: 'Delete', icon: 'fa-trash' }
            ];
            
            actions.forEach(action => {
                const item = document.createElement('div');
                item.className = 'dropdown-item';
                item.style.padding = '10px 15px';
                item.style.cursor = 'pointer';
                item.style.display = 'flex';
                item.style.alignItems = 'center';
                item.style.gap = '10px';
                item.innerHTML = `<i class="fas ${action.icon}"></i> ${action.text}`;
                
                item.addEventListener('mouseover', () => {
                    item.style.backgroundColor = 'var(--color-bg-tertiary)';
                });
                
                item.addEventListener('mouseout', () => {
                    item.style.backgroundColor = 'transparent';
                });
                
                item.addEventListener('click', () => {
                    if (action.text === 'Delete') {
                        const confirmDelete = confirm(`Are you sure you want to delete "${documentName}"?`);
                        if (!confirmDelete) return;
                
                        const form = document.createElement('form');
                        form.method = 'POST';
                        form.action = '/delete_file';
                
                        const input = document.createElement('input');
                        input.type = 'hidden';
                        input.name = 'filename';
                        input.value = documentName;
                
                        form.appendChild(input);
                        document.body.appendChild(form);
                        form.submit();
                    } else if (action.text === 'Download') {
                        const link = document.createElement('a');
                        link.href = `/download/${encodeURIComponent(documentName)}`;
                        link.download = documentName;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    } else {
                        alert(`${action.text} action for ${documentName}`);
                    }
                
                    // ✅ FIXED: Only remove dropdown if it's still in the DOM
                    if (document.body.contains(dropdown)) {
                        document.body.removeChild(dropdown);
                    }
                });
                
                
                dropdown.appendChild(item);
            });
            
            document.body.appendChild(dropdown);
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function closeDropdown(e) {
                if (!dropdown.contains(e.target) && e.target !== btn) {
                    if (document.body.contains(dropdown)) {
                        document.body.removeChild(dropdown);
                    }
                    document.removeEventListener('click', closeDropdown);
                }
            });
        });
    });
});
