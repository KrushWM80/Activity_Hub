/**
 * Template Engine
 * Generates HTML output from evaluation data
 */

class TemplateEngine {
  generateHTML(evaluation, score, userInfo = {}) {
    const now = new Date();
    const date = now.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });

    const scoreColor = score >= 80 ? '#4CAF50' : score >= 70 ? '#FFC107' : '#FF9800';
    const scoreLabel = score >= 80 ? 'Exceeds Expectations' : score >= 70 ? 'Meets Expectations' : 'Developing';

    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Evaluation - ${userInfo.name || 'Employee'}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }

        header {
            border-bottom: 3px solid #1976d2;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }

        .header-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
        }

        h1 {
            font-size: 28px;
            color: #1976d2;
            margin-bottom: 5px;
        }

        .user-info {
            text-align: right;
        }

        .user-info p {
            color: #666;
            margin: 2px 0;
        }

        .score-badge {
            background: ${scoreColor};
            color: white;
            padding: 10px 15px;
            border-radius: 4px;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
        }

        .score-value {
            font-size: 36px;
            font-weight: bold;
        }

        .score-label {
            font-size: 14px;
            margin-top: 5px;
        }

        .meta-info {
            display: flex;
            gap: 40px;
            color: #666;
            font-size: 14px;
            margin-top: 10px;
        }

        .meta-item {
            display: flex;
            gap: 5px;
        }

        .meta-label {
            font-weight: 600;
        }

        /* Executive Summary */
        .section {
            margin: 40px 0;
            padding: 20px;
            background: #f9f9f9;
            border-left: 4px solid #1976d2;
            border-radius: 4px;
        }

        .section h2 {
            color: #1976d2;
            font-size: 20px;
            margin-bottom: 15px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 10px;
        }

        .section h3 {
            color: #333;
            font-size: 16px;
            margin-top: 15px;
            margin-bottom: 10px;
        }

        .section p {
            color: #555;
            margin-bottom: 12px;
            line-height: 1.8;
        }

        .section ul {
            margin-left: 20px;
            margin-bottom: 15px;
        }

        .section li {
            margin-bottom: 8px;
            color: #555;
        }

        /* Competencies */
        .competencies-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .competency-card {
            background: white;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #4CAF50;
        }

        .competency-card h4 {
            color: #1976d2;
            margin-bottom: 10px;
            font-size: 14px;
        }

        .competency-card ul {
            margin-left: 15px;
        }

        .competency-card li {
            font-size: 13px;
            color: #666;
            margin-bottom: 5px;
        }

        /* Projects */
        .project {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 4px;
            border-left: 4px solid #1976d2;
        }

        .project h3 {
            color: #1976d2;
            margin-bottom: 10px;
        }

        .project-meta {
            display: flex;
            gap: 15px;
            margin: 10px 0;
            font-size: 13px;
            color: #666;
        }

        .project-meta span {
            background: #e3f2fd;
            padding: 3px 8px;
            border-radius: 3px;
        }

        .project-field {
            margin: 12px 0;
        }

        .project-label {
            font-weight: 600;
            color: #333;
            font-size: 13px;
        }

        .project-value {
            color: #666;
            margin-top: 3px;
        }

        /* Statistics */
        .statistics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }

        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #1976d2;
        }

        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }

        /* Footer */
        footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
            color: #999;
            font-size: 12px;
        }

        /* Print styles */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            .container {
                box-shadow: none;
                padding: 0;
            }
        }

        @media (max-width: 600px) {
            .header-top {
                flex-direction: column;
            }
            .user-info {
                text-align: left;
                margin-top: 15px;
            }
            .statistics {
                grid-template-columns: repeat(2, 1fr);
            }
            .competencies-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-top">
                <div>
                    <h1>Performance Evaluation</h1>
                    <div class="meta-info">
                        <div class="meta-item">
                            <span class="meta-label">Period:</span>
                            <span>${evaluation.metadata.period}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Generated:</span>
                            <span>${date}</span>
                        </div>
                    </div>
                </div>
                <div>
                    <div class="score-badge">
                        <div class="score-value">${score}</div>
                        <div class="score-label">${scoreLabel}</div>
                    </div>
                </div>
            </div>
            <div class="user-info">
                <p><strong>${userInfo.name || 'Employee'}</strong></p>
                <p>${userInfo.title || 'Not specified'}</p>
            </div>
        </header>

        <!-- Executive Summary -->
        <section class="section">
            <h2>Executive Summary</h2>
            ${evaluation.summary.split('\n\n').map(p => `<p>${p}</p>`).join('')}
        </section>

        <!-- Leadership Competencies -->
        ${evaluation.competencies ? `
        <section class="section">
            <h2>Leadership Competencies</h2>
            <div class="competencies-grid">
                ${evaluation.competencies.split('###').filter(c => c.trim()).map(competency => {
                    const lines = competency.trim().split('\n');
                    const title = lines[0];
                    const items = lines.slice(1).filter(l => l.startsWith('•'));
                    return `
                        <div class="competency-card">
                            <h4>${title}</h4>
                            <ul>
                                ${items.map(item => `<li>${item.replace('•', '').trim()}</li>`).join('')}
                            </ul>
                        </div>
                    `;
                }).join('')}
            </div>
        </section>
        ` : ''}

        <!-- Project Portfolio -->
        <section class="section">
            <h2>Project Portfolio</h2>
            ${evaluation.projectPortfolio.split('## ').filter(p => p.trim()).map(project => {
                const lines = project.trim().split('\n');
                const title = lines[0];
                const content = lines.slice(1).join('\n');
                return `
                    <div class="project">
                        <h3>${title}</h3>
                        ${content.split('\n\n').map(section => {
                            if (section.startsWith('**') && section.includes(':')) {
                                const [label, ...valueParts] = section.split(':');
                                return `<div class="project-field"><div class="project-label">${label.replace(/\*\*/g, '')}</div><div class="project-value">${valueParts.join(':').trim()}</div></div>`;
                            }
                            return `<p>${section}</p>`;
                        }).join('')}
                    </div>
                `;
            }).join('')}
        </section>

        <!-- Statistics -->
        ${evaluation.statistics ? `
        <section class="section">
            <h2>Summary Statistics</h2>
            <div class="statistics">
                <div class="stat-card">
                    <div class="stat-value">${evaluation.statistics.totalProjects}</div>
                    <div class="stat-label">Total Projects</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${evaluation.statistics.totalHours}</div>
                    <div class="stat-label">Hours Invested</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${evaluation.statistics.totalTeamMembers}</div>
                    <div class="stat-label">Team Members</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${evaluation.statistics.departments.length}</div>
                    <div class="stat-label">Departments</div>
                </div>
            </div>
        </section>
        ` : ''}

        <footer>
            <p>This evaluation was generated by the Performance Evaluation System on ${date}</p>
            <p>For more information or to make edits, please revisit the evaluation system interface.</p>
        </footer>
    </div>
</body>
</html>
    `;
  }
}

export default new TemplateEngine();
