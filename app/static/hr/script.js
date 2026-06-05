class HRDashboard {
    constructor() {
        this.form = document.getElementById('bulkForm');
        this.resultsSection = document.getElementById('resultsSection');
        this.initEventListeners();
    }

    initEventListeners() {
        this.form.addEventListener('submit', (e) => this.handleBulkSubmit(e));
    }

    async handleBulkSubmit(e) {
        e.preventDefault();
        const files = Array.from(document.getElementById('bulkFiles').files);
        
        if (files.length > 10) {
            alert('Maximum 10 files allowed');
            return;
        }

        const formData = new FormData();
        files.forEach(file => formData.append('resumes', file));

        try {
            this.showLoading();
            const response = await fetch('http://localhost:8000/api/bulk-screen', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) throw new Error('Bulk screening failed');
            
            const result = await response.json();
            this.displayBulkResults(result.candidates);
        } catch (error) {
            alert('Error in bulk screening: ' + error.message);
        } finally {
            this.hideLoading();
        }
    }

    showLoading() {
        const btn = this.form.querySelector('button');
        btn.textContent = '⏳ Screening Resumes...';
        btn.disabled = true;
    }

    hideLoading() {
        const btn = this.form.querySelector('button');
        btn.textContent = '🚀 Screen All Resumes';
        btn.disabled = false;
    }

    displayBulkResults(candidates) {
        this.resultsSection.style.display = 'block';
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Update stats
        const total = candidates.length;
        const avgScore = candidates.reduce((sum, c) => sum + c.ats_score, 0) / total;
        const topScore = Math.max(...candidates.map(c => c.ats_score));

        document.getElementById('totalCandidates').textContent = total;
        document.getElementById('avgScore').textContent = avgScore.toFixed(1) + '%';
        document.getElementById('topScore').textContent = topScore.toFixed(1) + '%';

        // Update table
        this.renderCandidatesTable(candidates.slice(0, 10));

        // Render charts
        this.renderDistributionChart(candidates);
        this.renderSkillsChart(candidates);
    }

    renderCandidatesTable(candidates) {
        const tbody = document.querySelector('#candidatesTable tbody');
        tbody.innerHTML = candidates.map((candidate, index) => `
            <tr>
                <td>${index + 1} 🥇</td>
                <td>${candidate.filename}</td>
                <td><span class="score-badge score-${this.getScoreCategory(candidate.ats_score)}">${candidate.ats_score}%</span></td>
                <td>${(candidate.skill_match * 100).toFixed(0)}%</td>
                <td>${candidate.experience_years.toFixed(1)} yrs</td>
                <td><button class="action-btn" onclick="viewDetails(${index})">View Details</button></td>
            </tr>
        `).join('');
    }

    getScoreCategory(score) {
        if (score >= 90) return '90+';
        if (score >= 80) return '80-89';
        return 'below-80';
    }

    renderDistributionChart(candidates) {
        const ctx = document.getElementById('distributionChart').getContext('2d');
        const scores = candidates.map(c => c.ats_score);
        new Chart(ctx, {
            type: 'histogram',
            data: {
                datasets: [{
                    label: 'ATS Scores',
                    data: scores,
                    backgroundColor: 'rgba(240, 147, 251, 0.6)',
                    borderColor: '#f093fb',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { title: { display: true, text: 'ATS Score (%)' } },
                    y: { title: { display: true, text: 'Number of Candidates' } }
                }
            }
        });
    }

    renderSkillsChart(candidates) {
        // Aggregate top skills
        const allSkills = candidates.flatMap(c => c.skills.extracted_skills.slice(0, 5));
        const skillCounts = allSkills.reduce((acc, skill) => {
            acc[skill] = (acc[skill] || 0) + 1;
            return acc;
        }, {});
        
        const sortedSkills = Object.entries(skillCounts)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10);

        const ctx = document.getElementById('skillsChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedSkills.map(([skill]) => skill),
                datasets: [{
                    label: 'Candidates with Skill',
                    data: sortedSkills.map(([, count]) => count),
                    backgroundColor: '#f093fb'
                }]
            },
            options: {
                responsive: true,
                indexAxis: 'y',
                scales: { x: { beginAtZero: true } }
            }
        });
    }
}

// Global function for detail view (placeholder)
function viewDetails(index) {
    alert(`View detailed analysis for candidate ${index + 1}`);
}

new HRDashboard();