# TaskFlow UX/UI Specification

**Status:** Design specification  
**Product:** TaskFlow Todo Management Web Application  
**Design direction:** Minimalist, modern, professional, clean, and focused  
**Implementation target:** HTML, Tailwind CSS, Vanilla JavaScript

## 1. Design Principles

1. **Focus:** Keep the primary action—understanding and managing tasks—obvious.
2. **Clarity:** Use concise labels, predictable controls, and visible status feedback.
3. **Trust:** Make account state, task ownership, errors, and successful actions understandable.
4. **Accessibility:** Support keyboard navigation, screen readers, readable contrast, and visible focus.
5. **Responsive first:** Preserve task visibility and action usability from small mobile screens through desktop layouts.
6. **Progressive disclosure:** Show essential information first; reveal editing and destructive actions only when needed.

## 2. Visual Design System

### Color palette

Use a light neutral foundation with blue as the primary accent and violet as a restrained secondary accent.

| Token | Suggested Tailwind role | Use |
|---|---|---|
| `canvas` | `bg-slate-50` | Page background |
| `surface` | `bg-white` | Cards, forms, panels |
| `surface-muted` | `bg-slate-100` | Subtle sections and disabled backgrounds |
| `border` | `border-slate-200` | Card and input boundaries |
| `text-primary` | `text-slate-900` | Headings and primary content |
| `text-secondary` | `text-slate-600` | Supporting text |
| `text-muted` | `text-slate-500` | Hints and metadata |
| `brand` | `blue-600` | Primary actions and active navigation |
| `brand-hover` | `blue-700` | Hover/pressed primary actions |
| `accent` | `violet-600` | Optional emphasis and visual differentiation |
| `success` | `emerald-600` | Completed status and success feedback |
| `warning` | `amber-600` | Caution or pending attention |
| `danger` | `red-600` | Delete actions and errors |

Color must not be the only indication of status; pair colors with text, icons, or accessible labels.

### Typography

- Use a modern sans-serif system font stack.
- Page title: prominent, semibold, responsive size.
- Section heading: semibold with clear hierarchy.
- Body: comfortable line height and readable contrast.
- Labels: medium weight and associated explicitly with controls.
- Metadata: smaller text, never the only source of essential information.

### Shape, spacing, and elevation

- Use rounded cards and controls with consistent medium radius.
- Use a restrained shadow on elevated cards and dialogs; avoid excessive decoration.
- Use a consistent spacing scale based on Tailwind utilities.
- Keep touch targets approximately 44px or larger.
- Use a visible 2px focus ring with sufficient contrast.

## 3. Application Shell and Navigation

### Desktop

- Center the application within a comfortable max-width container.
- Top navigation contains the TaskFlow wordmark, current section links, and logout action.
- Main content uses a dashboard grid and task workspace.
- Keep the primary “New task” action visible near the task list heading.

### Mobile

- Use a compact top bar with wordmark and menu or section controls.
- Stack dashboard cards vertically or in a two-column compact grid where space permits.
- Keep “New task” as a full-width or prominent action.
- Place edit, status, and delete controls in a clear wrapping action row.
- Avoid horizontal scrolling for forms, cards, and task content.

### Navigation states

- Active navigation uses brand color, weight, and an additional indicator.
- Unauthenticated users see only auth navigation.
- Authenticated users see dashboard, tasks, and logout.
- On `401`, clear the authenticated UI state and transition to signin with a safe message.

## 4. Screen Specifications

## 4.1 Signup Page

**Purpose:** Let a new visitor create a private TaskFlow account.

### Layout

- Center a single auth card on the light canvas.
- Show TaskFlow wordmark, concise value statement, and signup heading.
- Place the form in a single column.
- Provide a link to the signin page below the primary action.

### Content and controls

- Canonical login identifier field, using the decision recorded in the implementation contract.
- Password field with visible label and accessible guidance.
- Optional password confirmation only if included in the approved API contract.
- Primary “Create account” button.
- Inline field errors and a top-level safe error region.

### States

- Default, focused, submitting, success, duplicate identifier, invalid input, and service error.
- Disable or protect repeated submission while the request is in flight.
- On success, transition to signin or the authenticated view according to the approved auth flow.

### Accessibility

- Each input has a persistent visible label.
- Errors use `aria-describedby` and are announced through an appropriate live region.
- Focus moves to the first invalid field after server validation errors.
- Password guidance does not expose or echo the password.

## 4.2 Signin Page

**Purpose:** Let a registered user securely start an authenticated session.

### Layout

- Reuse the signup auth-card structure for familiarity.
- Use a concise heading and supporting text.
- Place the signin form in a single column.
- Provide a link to signup.

### Content and controls

- Canonical login identifier field.
- Password field.
- Primary “Sign in” button.
- Safe generic authentication error region.

### States

- Default, submitting, invalid fields, invalid credentials, throttled request, service unavailable, and success.
- Never display whether the identifier or password alone was incorrect.
- Do not display or store the JWT in the page or JavaScript state.

## 4.3 Main Dashboard

**Purpose:** Give the authenticated user an immediate view of workload and progress.

### Layout

1. Page heading with short contextual greeting or neutral supporting text.
2. Statistics row/grid.
3. Task workspace heading with task creation button and filters.
4. Task list or empty state.

### Required statistics

- **Total tasks:** all tasks owned by the authenticated user.
- **Pending tasks:** incomplete tasks owned by the authenticated user.
- **Completed tasks:** completed tasks owned by the authenticated user.

Each statistic card includes a text label and numeric value. Do not rely on color alone.

### Task workspace

- “Tasks” heading and optional result count.
- Primary “New task” button.
- Filter controls: All, Pending, Completed.
- Task list with status, title, metadata if approved, and actions.
- Loading, error, and empty states.

### Responsive behavior

- Desktop: three statistic cards in a row and task controls aligned horizontally.
- Tablet: cards wrap while preserving readable widths.
- Mobile: cards stack or use a compact two-column layout; filters may become a full-width segmented control or select.

## 4.4 Create Todo Form

**Purpose:** Capture a new incomplete task.

### Presentation

- Prefer a modal/dialog on desktop and a full-width sheet or page section on mobile.
- Keep the task form short and focused.
- Use a clear heading: “Create task.”

### Controls

- Required task title field.
- Optional description only if included in the approved MVP data model.
- Primary “Create task” action.
- Secondary “Cancel” action.

### Behavior

- New tasks are visibly marked pending/incomplete after creation.
- Preserve entered values if validation fails.
- Close the dialog only after successful creation.
- Refresh or update dashboard statistics and the visible task list.

### Accessibility

- Use a dialog label and description where modal presentation is used.
- Trap focus while open and return focus to the “New task” button on close.
- Escape closes the dialog when safe.
- Do not remove the form from the accessibility tree while errors are displayed.

## 4.5 Edit Todo Form

**Purpose:** Update approved fields on an owned task.

### Presentation

- Reuse the create form layout and styling.
- Heading identifies the action as “Edit task.”
- Prepopulate only editable fields.

### Behavior

- Preserve task ownership and completion state unless the approved interaction explicitly changes status through the status control.
- Show a saving state and prevent duplicate submissions.
- On success, update the task row/card and dashboard if relevant.
- On invalid input, retain the form and focus the first invalid field.

## 4.6 Empty Task State

**Purpose:** Help a user understand what to do when no tasks match the current view.

### Content

- Friendly, concise heading such as “No tasks yet” for the all-tasks view.
- Supporting text explaining the next step.
- Primary “Create your first task” action.
- Use a simple neutral illustration or icon only if it improves comprehension.

### Filter-specific behavior

- If the user has tasks but the selected filter has no matches, say “No completed tasks” or “No pending tasks” and offer a way to change the filter.
- Do not imply that the account has no tasks when only a filter is empty.

## 4.7 Completed Tasks View

**Purpose:** Let users review tasks marked complete.

### Layout and content

- Reuse the main task workspace with the Completed filter active.
- Completed tasks use a clear status label and subdued styling.
- Preserve readable title text; do not rely solely on strikethrough.
- Provide an accessible “Mark as pending” or “Uncomplete” action.
- Retain edit and delete controls according to the approved task interaction.

### Empty state

- Explain that no tasks are currently completed.
- Provide a clear route back to All or Pending tasks.

## 4.8 Responsive Mobile Layout

### Mobile priorities

- Keep the current task count and primary action visible without excessive scrolling.
- Stack forms and statistic cards vertically.
- Use full-width inputs and buttons where appropriate.
- Keep task actions reachable without tiny icon-only targets.
- Use text labels or tooltips for unfamiliar icons.

### Breakpoint behavior

- **Small mobile:** one-column content, stacked controls, full-width primary actions.
- **Large mobile/tablet:** compact statistic grid, wrapping task actions, wider dialog/sheet.
- **Desktop:** centered max-width workspace, horizontal controls, elevated cards/dialogs.

### Mobile interaction rules

- Never require hover to discover an essential action.
- Avoid hover-only menus for edit, status, or delete.
- Use confirmation for destructive deletion, with a clear cancel action.
- Maintain visible focus for keyboard and switch-control users.

## 5. Reusable Component List

### Layout components

- `AppShell`: authenticated page frame, navigation, content container.
- `AuthLayout`: centered auth card and public navigation.
- `TopNavigation`: wordmark, active section, logout.
- `PageHeader`: heading, supporting text, and primary action slot.
- `ResponsiveContainer`: max-width and horizontal padding rules.
- `Stack`/`Grid`: consistent responsive spacing patterns.

### Data display components

- `StatCard`: label, value, optional icon, semantic status.
- `TaskList`: loading, populated, filtered, and empty states.
- `TaskCard` or `TaskRow`: title, status, metadata, and actions.
- `StatusBadge`: text-plus-color completion indicator.
- `FilterControl`: All/Pending/Completed selection.
- `EmptyState`: message, explanation, and action.
- `LoadingState`: non-blocking progress indicator with accessible status.

### Form and interaction components

- `TextField`: label, hint, input, error, disabled, and focus states.
- `PasswordField`: password input with accessible guidance.
- `TextareaField`: optional task description if approved.
- `PrimaryButton`: main action with loading/disabled states.
- `SecondaryButton`: cancel and lower-emphasis actions.
- `DangerButton`: destructive action with confirmation flow.
- `IconButton`: only for universally recognizable actions and always with an accessible name.
- `TaskForm`: shared create/edit form configuration.
- `Dialog`: modal focus management, close behavior, and responsive presentation.
- `Toast` or `InlineNotice`: success and non-field error feedback.
- `ConfirmDialog`: explicit delete confirmation.

### State and utility modules

- `ApiClient`: same-origin fetch, credentials, CSRF header, response/error normalization.
- `AuthState`: authenticated/unauthenticated transitions without exposing JWT.
- `FormState`: submitting, validation, success, and error state management.
- `TaskState`: list, filter, mutation, and refresh state.
- `DashboardState`: statistics loading and refresh state.
- `FocusManager`: focus restoration and invalid-field focus.

## 6. Interaction and Feedback Rules

- Every network action has a visible submitting/loading state.
- Success feedback is concise and does not interrupt the next action.
- Errors explain what the user can do next and never expose internals.
- Field errors appear near their fields; general errors appear in a live region.
- Delete requires confirmation and updates the list/counts after success.
- Completion toggles should feel immediate but must reconcile with the API response.
- After a `401`, clear protected UI state and guide the user to signin.
- After a `403` CSRF/origin failure, show a safe retry message and do not silently repeat the request.

## 7. Accessibility Requirements

- Meet the approved accessibility direction for meaningful labels, keyboard access, and visually distinct states.
- Use semantic headings in logical order.
- Associate labels, hints, and errors with form controls.
- Provide `aria-live` regions for async status and error feedback without over-announcing.
- Ensure focus indicators are visible against white and light-grey surfaces.
- Maintain sufficient text and control contrast.
- Provide text labels for Total, Pending, and Completed; color is supplementary.
- Ensure dialogs have accessible names, focus trapping, Escape handling, and focus restoration.
- Make all essential actions keyboard-operable.
- Respect reduced-motion preferences for non-essential animations.

## 8. UX Validation Checklist

- Signup and signin work with keyboard-only navigation.
- Invalid signup, signin, and todo input is understandable and field-associated.
- Dashboard displays total, pending, completed, task list, creation action, and filters.
- Create, edit, delete, complete, and uncomplete actions provide clear feedback.
- Empty all-task and empty-filter states are distinct and actionable.
- Completed tasks remain readable and offer an accessible uncomplete action.
- Mobile layouts avoid horizontal scrolling and preserve usable touch targets.
- Desktop layouts use consistent cards, spacing, typography, and action hierarchy.
- Protected UI never displays stale task data after logout or `401`.

