// ==========================================
// PHASE 2: API Integration for Links Management
// ==========================================

const API_LINKS = 'http://localhost:8001/api/links';

function getCurrentUser() {
  return { id: 'krush', email: 'krush@walmart.com', name: 'Krush', isAdmin: true };
}

async function loadManagedLinks() {
  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS, {
      method: 'GET',
      headers: {
        'X-User-ID': user.id,
        'X-User-Email': user.email,
        'X-User-Name': user.name,
        'X-User-Role': 'admin'
      }
    });
    if (!response.ok) throw new Error('Failed to fetch links');
    const links = await response.json();
    renderManagedLinks(links);
  } catch (error) {
    console.error('Error loading links:', error);
    alert('Failed to load links: ' + error.message);
  }
}

function renderManagedLinks(links) {
  const container = document.querySelector('.item-list');
  if (!container) return;
  
  container.innerHTML = links.map(link => `
    <div class="list-item" data-link-id="${link.id}">
      <div class="item-info">
        <h4>${link.name}</h4>
        <p>Creator: ${link.creator_name || link.creator_email} | Privacy: <span class="badge badge-${link.privacy_type}">${link.privacy_type}</span> | Health: <span class="badge badge-${link.health_status}">${link.health_status}</span></p>
        <p style="font-size: 0.85rem; color: var(--gray-600);">URL: ${link.url}<br>Modified: ${new Date(link.modified_date).toLocaleDateString()}</p>
      </div>
      <div class="item-actions" style="display: flex; flex-direction: column; gap: var(--space-2);">
        <div style="display: flex; gap: var(--space-2);">
          <button class="action-btn edit-btn" onclick="editLink('${link.id}')">Edit</button>
          <button class="action-btn delete-btn" onclick="deleteLink('${link.id}')">Delete</button>
        </div>
        <button class="action-btn" style="background: var(--walmart-blue-light); color: white; font-size: 0.75rem;" onclick="checkLinkHealth('${link.id}')">Check Health</button>
      </div>
    </div>
  `).join('');
}

async function checkDuplicateUrl(url) {
  if (!url) return { isDuplicate: false };
  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS + '/check/duplicate?url=' + encodeURIComponent(url), {
      method: 'GET',
      headers: { 'X-User-ID': user.id, 'X-User-Email': user.email, 'X-User-Role': 'admin' }
    });
    return await response.json();
  } catch (error) {
    console.error('Error checking duplicate:', error);
    return { isDuplicate: false };
  }
}

async function submitLink(event) {
  event.preventDefault();
  const form = event.target;
  const name = form.querySelector('input[placeholder="Display name"]').value;
  const url = form.querySelector('input[placeholder="https://example.com"]').value;
  const category = form.querySelector('select').value;
  const privacyType = form.querySelector('#linkPrivacy') ? form.querySelector('#linkPrivacy').value : 'private';
  
  const dupCheck = await checkDuplicateUrl(url);
  if (dupCheck.isDuplicate) {
    alert('Link already exists!\n\nURL: ' + dupCheck.link.url + '\nCreator: ' + dupCheck.link.creator_email);
    return;
  }

  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': user.id,
        'X-User-Email': user.email,
        'X-User-Name': user.name,
        'X-User-Role': 'admin'
      },
      body: JSON.stringify({
        name: name,
        url: url,
        category: category,
        privacy_type: privacyType,
        description: form.querySelector('textarea') ? form.querySelector('textarea').value : '',
        is_admin_created: true
      })
    });

    if (response.status === 409) { alert('This URL already exists!'); return; }
    if (!response.ok) { const error = await response.json(); throw new Error(error.error || 'Failed to create link'); }

    document.getElementById('linkSuccessMessage').style.display = 'block';
    await loadManagedLinks();
    form.reset();
    setTimeout(() => hideModal('addLinkModal'), 1500);
  } catch (error) {
    console.error('Error creating link:', error);
    alert('Failed to create link: ' + error.message);
  }
}

async function editLink(linkId) {
  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS + '/' + linkId, {
      method: 'GET',
      headers: { 'X-User-ID': user.id, 'X-User-Email': user.email, 'X-User-Role': 'admin' }
    });
    const link = await response.json();
    const modal = document.createElement('div');
    modal.id = 'editLinkModal';
    modal.className = 'modal';
    modal.innerHTML = '<div class="modal-content"><div class="modal-header"><h3>Edit Link</h3><button class="close-btn" onclick="hideModal(\'editLinkModal\')">×</button></div><form onsubmit="submitLinkEdit(event, \'' + linkId + '\')" style="padding: var(--space-6);"><div class="form-grid"><div class="form-group"><label class="form-label">Link Name</label><input type="text" class="form-input" value="' + link.name + '" required></div><div class="form-group"><label class="form-label">Privacy</label><select class="form-input"><option value="private" ' + (link.privacy_type === 'private' ? 'selected' : '') + '>Private</option><option value="shared" ' + (link.privacy_type === 'shared' ? 'selected' : '') + '>Shared</option><option value="public" ' + (link.privacy_type === 'public' ? 'selected' : '') + '>Public</option></select></div></div><div class="form-group"><label class="form-label">URL</label><input type="url" class="form-input" value="' + link.url + '" required></div><div class="form-group"><label class="form-label">Description</label><textarea class="form-input" style="min-height: 80px;">' + (link.description || '') + '</textarea></div><div style="display: flex; gap: var(--space-4); justify-content: flex-end; margin-top: var(--space-6);"><button type="button" class="btn-secondary" onclick="hideModal(\'editLinkModal\')">Cancel</button><button type="submit" class="btn-primary">Save Changes</button></div></form></div>';
    document.body.appendChild(modal);
    showModal('editLinkModal');
  } catch (error) {
    console.error('Error fetching link:', error);
    alert('Failed to load link details');
  }
}

async function submitLinkEdit(event, linkId) {
  event.preventDefault();
  const form = event.target;
  const name = form.querySelector('input[type="text"]').value;
  const url = form.querySelector('input[type="url"]').value;
  const privacyType = form.querySelector('select').value;
  const description = form.querySelector('textarea').value;

  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS + '/' + linkId, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'X-User-ID': user.id, 'X-User-Email': user.email, 'X-User-Role': 'admin' },
      body: JSON.stringify({ name: name, url: url, privacy_type: privacyType, description: description })
    });
    if (!response.ok) { const error = await response.json(); throw new Error(error.error); }
    alert('Link updated successfully!');
    hideModal('editLinkModal');
    await loadManagedLinks();
  } catch (error) {
    console.error('Error updating link:', error);
    alert('Failed to update link: ' + error.message);
  }
}

async function deleteLink(linkId) {
  if (!confirm('Are you sure you want to delete this link?')) return;
  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS + '/' + linkId, {
      method: 'DELETE',
      headers: { 'X-User-ID': user.id, 'X-User-Email': user.email, 'X-User-Role': 'admin' }
    });
    if (!response.ok) throw new Error('Failed to delete link');
    alert('Link deleted successfully!');
    await loadManagedLinks();
  } catch (error) {
    console.error('Error deleting link:', error);
    alert('Failed to delete link: ' + error.message);
  }
}

async function checkLinkHealth(linkId) {
  try {
    const user = getCurrentUser();
    const response = await fetch(API_LINKS + '/' + linkId + '/health-check', {
      method: 'POST',
      headers: { 'X-User-ID': user.id, 'X-User-Email': user.email, 'X-User-Role': 'admin' }
    });
    const result = await response.json();
    alert('Health Check Result:\n\nStatus: ' + result.status + '\nResponse Time: ' + result.responseTime + 'ms\nError: ' + (result.errorMessage || 'None'));
    await loadManagedLinks();
  } catch (error) {
    console.error('Error checking health:', error);
    alert('Failed to check link health: ' + error.message);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const linksTab = document.getElementById('links');
  if (linksTab && linksTab.classList.contains('active')) {
    loadManagedLinks();
  }
});
