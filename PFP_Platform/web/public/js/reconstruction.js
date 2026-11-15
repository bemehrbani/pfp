/**
 * Legacy dynamic-import stub for stale cached HTML clients still referencing `js/reconstruction.js`.
 * Canonical entry point is `<script type="module" src="js/reconstruction/main.js">`.
 */
import('./reconstruction/main.js').catch((err) => {
  console.error('Failed to load modular reconstruction engine:', err);
});
