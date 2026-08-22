export function toast(message, type = 'info') {
  window.dispatchEvent(new CustomEvent('app:toast', { detail: { message, type } }))
}
