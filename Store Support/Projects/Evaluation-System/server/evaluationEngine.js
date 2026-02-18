/**
 * Evaluation Engine
 * Generates narrative and metrics from structured project data
 */

import { competencies } from './config.js';

class EvaluationEngine {
  /**
   * Generate executive summary from projects
   */
  generateExecutiveSummary(projects, summary, period) {
    const projectCount = summary.totalProjects;
    const hoursLabel = summary.totalHours > 0 ? ` across ${summary.totalHours}+ hours invested` : '';
    const departmentLabel = summary.departments.length > 0 
      ? ` across ${summary.departments.length} departments (${summary.departments.join(',')})`
      : '';

    const statuses = Object.entries(summary.projectsByStatus)
      .map(([status, count]) => `${count} ${status}`)
      .join(', ');

    return `
This evaluation period demonstrates exceptional performance across ${projectCount} major initiatives, delivering measurable business impact and strategic leadership${hoursLabel}. The portfolio reflects strong execution across multiple domains with clear alignment to leadership competencies.

**Portfolio Overview:** ${statuses}${departmentLabel}

**Total Team Coordination:** ${summary.totalTeamMembers}+ collaborators engaged across initiatives

**Key Metrics:**
${this.formatMetrics(summary.metrics)}

This work demonstrates consistent application of all four leadership competencies: Respect for the Individual through cross-functional collaboration, Act with Integrity through transparent execution, Service to Customer/Member through measurable outcomes, and Strive for Excellence through continuous improvement and adoption of modern practices.
    `.trim();
  }

  /**
   * Format metrics into readable bullet points
   */
  formatMetrics(metrics) {
    if (!metrics || metrics.length === 0) {
      return '• Multiple measurable outcomes delivered';
    }

    return metrics
      .map(m => {
        let line = `• ${m.label}: ${m.value}`;
        if (m.businessValue) {
          line += ` (${m.businessValue})`;
        }
        return line;
      })
      .join('\n');
  }

  /**
   * Extract competency evidence from projects
   */
  extractCompetencyEvidence(projects) {
    const evidence = {
      'Respect for the Individual': [],
      'Act with Integrity': [],
      'Service to Customer/Member': [],
      'Strive for Excellence': []
    };

    projects.forEach(project => {
      if (project.competency_respect) {
        evidence['Respect for the Individual'].push(project.competency_respect);
      }
      if (project.competency_integrity) {
        evidence['Act with Integrity'].push(project.competency_integrity);
      }
      if (project.competency_service) {
        evidence['Service to Customer/Member'].push(project.competency_service);
      }
      if (project.competency_excellence) {
        evidence['Strive for Excellence'].push(project.competency_excellence);
      }
    });

    return evidence;
  }

  /**
   * Generate competency section narrative
   */
  generateCompetencySection(evidence) {
    const sections = [];

    competencies.forEach(competency => {
      const compEvidence = evidence[competency.name] || [];
      if (compEvidence.length > 0) {
        sections.push(`
### ${competency.icon} ${competency.name}

${compEvidence.map(e => `• ${e}`).join('\n')}
        `.trim());
      }
    });

    return sections.join('\n\n');
  }

  /**
   * Generate project portfolio section
   */
  generateProjectPortfolio(projects) {
    const sections = projects.map(project => {
      let section = `
## ${project.project_name}

**Status:** ${project.project_status || 'Not specified'}

${project.description}

**Key Accomplishment:** ${project.accomplishment}
      `.trim();

      if (project.metrics_value && project.metrics_label) {
        section += `\n\n**Impact:** ${project.metrics_value} ${project.metrics_label}`;
      }

      if (project.business_value) {
        section += `\n**Business Value:** ${project.business_value}`;
      }

      if (project.team_size || project.team_departments) {
        section += `\n\n**Collaboration:**`;
        if (project.team_size) {
          section += `\n• Team Members: ${project.team_size}`;
        }
        if (project.team_departments) {
          section += `\n• Departments: ${project.team_departments}`;
        }
      }

      if (project.challenges_faced) {
        section += `\n\n**Challenges & Solutions:** ${project.challenges_faced}`;
      }

      return section;
    });

    return sections.join('\n\n');
  }

  /**
   * Generate complete evaluation document
   */
  generateEvaluation(projects, summary, userInfo = {}) {
    const competencyEvidence = this.extractCompetencyEvidence(projects);
    const executiveSummary = this.generateExecutiveSummary(projects, summary);
    const competencySection = this.generateCompetencySection(competencyEvidence);
    const projectPortfolio = this.generateProjectPortfolio(projects);

    return {
      metadata: {
        generatedDate: new Date().toISOString(),
        period: userInfo.period || 'Custom',
        name: userInfo.name || 'Employee',
        title: userInfo.title || 'Not specified'
      },
      summary: executiveSummary,
      competencies: competencySection,
      projectPortfolio: projectPortfolio,
      statistics: {
        totalProjects: summary.totalProjects,
        projectsByStatus: summary.projectsByStatus,
        totalHours: summary.totalHours,
        totalTeamMembers: summary.totalTeamMembers,
        departments: summary.departments
      }
    };
  }

  /**
   * Calculate evaluation score (0-100)
   */
  calculateScore(projects, summary) {
    let score = 50; // Base score

    // Projects with metrics
    const projectsWithMetrics = projects.filter(p => p.metrics_value).length;
    score += Math.min((projectsWithMetrics / projects.length) * 20, 20);

    // Collaboration breadth
    if (summary.departments.length >= 5) score += 15;
    else if (summary.departments.length >= 3) score += 10;
    else if (summary.departments.length >= 1) score += 5;

    // Team size
    if (summary.totalTeamMembers >= 40) score += 15;
    else if (summary.totalTeamMembers >= 20) score += 10;
    else if (summary.totalTeamMembers > 0) score += 5;

    // Production projects
    const productionProjects = projects.filter(p => 
      p.project_status === 'In Production' || p.project_status === 'Completed'
    ).length;
    score += Math.min((productionProjects / projects.length) * 20, 20);

    // Competency coverage
    const competencyFields = ['competency_respect', 'competency_integrity', 'competency_service', 'competency_excellence'];
    const avgCompetencyCoverage = projects.reduce((avg, p) => {
      const covered = competencyFields.filter(f => p[f]).length;
      return avg + (covered / competencyFields.length);
    }, 0) / projects.length;
    score += avgCompetencyCoverage * 10;

    return Math.min(Math.round(score), 100);
  }
}

export default new EvaluationEngine();
