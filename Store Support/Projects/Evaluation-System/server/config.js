/**
 * Evaluation System Configuration
 * Defines expected data fields and their purposes
 */

export const evaluationFields = {
  project_name: {
    label: "Project Name",
    description: "Name of the project or initiative",
    required: true,
    type: "text",
    category: "core",
    info: "The main project or business initiative you're reporting on"
  },
  project_status: {
    label: "Project Status",
    description: "Current status (Planning, Active, In Production, Completed, On Hold)",
    required: true,
    type: "select",
    options: ["Planning", "Active", "In Production", "Completed", "On Hold"],
    category: "core",
    info: "Current state of the project"
  },
  description: {
    label: "Project Description",
    description: "What the project does and its business purpose",
    required: true,
    type: "textarea",
    category: "core",
    info: "Brief explanation of project scope and business value"
  },
  accomplishment: {
    label: "Key Accomplishment",
    description: "Major achievement or deliverable completed",
    required: true,
    type: "textarea",
    category: "core",
    info: "Specific accomplishment during evaluation period"
  },
  metrics_value: {
    label: "Metric Value",
    description: "Quantifiable result (e.g., users served, value generated)",
    required: false,
    type: "number",
    category: "metrics",
    info: "Numeric value of business impact (e.g., 50000 for 50,000 users)"
  },
  metrics_label: {
    label: "Metric Label",
    description: "What the metric represents (e.g., Users Served, Annual Value)",
    required: false,
    type: "text",
    category: "metrics",
    info: "Description of what the metric measures"
  },
  business_value: {
    label: "Business Value",
    description: "Impact in dollars, users, or efficiency gain",
    required: false,
    type: "text",
    category: "metrics",
    info: "Quantified business benefit (e.g., $27M annual value, 10% efficiency gain)"
  },
  team_size: {
    label: "Team Size",
    description: "Number of collaborators/team members",
    required: false,
    type: "number",
    category: "collaboration",
    info: "How many people worked on this"
  },
  team_departments: {
    label: "Departments Involved",
    description: "Comma-separated list of departments involved",
    required: false,
    type: "text",
    category: "collaboration",
    info: "Cross-functional teams (e.g., Engineering, Product, Finance)"
  },
  start_date: {
    label: "Start Date",
    description: "When the project/work started",
    required: false,
    type: "date",
    category: "timeline",
    info: "Project start date (YYYY-MM-DD)"
  },
  end_date: {
    label: "End Date",
    description: "When the project/work ended or is planned to end",
    required: false,
    type: "date",
    category: "timeline",
    info: "Project end date or current date if ongoing"
  },
  hours_invested: {
    label: "Hours Invested",
    description: "Total hours spent on this project",
    required: false,
    type: "number",
    category: "timeline",
    info: "Approximate total hours invested"
  },
  competency_respect: {
    label: "Respect for Individual",
    description: "How this demonstrates respect for people and collaboration",
    required: false,
    type: "textarea",
    category: "competencies",
    info: "Team building, mentoring, relationship examples"
  },
  competency_integrity: {
    label: "Act with Integrity",
    description: "How this demonstrates ethics and accountability",
    required: false,
    type: "textarea",
    category: "competencies",
    info: "Compliance, transparency, accountability examples"
  },
  competency_service: {
    label: "Service to Customer/Member",
    description: "How this demonstrates customer focus and results",
    required: false,
    type: "textarea",
    category: "competencies",
    info: "User needs, data-driven decisions, business impact"
  },
  competency_excellence: {
    label: "Strive for Excellence",
    description: "How this demonstrates growth and continuous improvement",
    required: false,
    type: "textarea",
    category: "competencies",
    info: "Innovation, best practices, learning from feedback"
  },
  challenges_faced: {
    label: "Challenges Faced",
    description: "Obstacles overcome or lessons learned",
    required: false,
    type: "textarea",
    category: "narrative",
    info: "Difficulties and how they were addressed"
  },
  future_plans: {
    label: "Future Plans",
    description: "Next steps or planned enhancements",
    required: false,
    type: "textarea",
    category: "narrative",
    info: "What comes next for this project"
  }
};

export const evaluationPeriods = {
  quarterly: {
    label: "Quarterly",
    months: 3,
    description: "3-month performance summary"
  },
  midyear: {
    label: "Mid-Year",
    months: 6,
    description: "6-month performance review"
  },
  fy: {
    label: "Fiscal Year",
    months: 12,
    description: "Full fiscal year performance"
  },
  custom: {
    label: "Custom",
    months: 0,
    description: "Custom period evaluation"
  }
};

export const competencies = [
  {
    name: "Respect for the Individual",
    icon: "👥",
    description: "Team building, relationships, mentoring, development"
  },
  {
    name: "Act with Integrity",
    icon: "🤝",
    description: "Ethics, compliance, accountability, servant leadership"
  },
  {
    name: "Service to Customer/Member",
    icon: "💼",
    description: "Results-focused, data-driven, omni-merchant mindset"
  },
  {
    name: "Strive for Excellence",
    icon: "⭐",
    description: "Growth mindset, continuous improvement, digital disruption"
  }
];

export default {
  evaluationFields,
  evaluationPeriods,
  competencies
};
