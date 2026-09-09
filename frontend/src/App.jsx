import { useEffect, useState } from "react";
import { createAssessment, fetchDashboard } from "./api";

const initialForm = {
  region: "",
  hazard_type: "Flood",
  event_severity: 5,
  exposure_index: 0.5,
  vulnerability_index: 0.5,
  preparedness_index: 0.5,
  indicators: [
    { name: "Rainfall Anomaly", value: 60, weight: 0.5, unit: "%" },
    { name: "Hydrology Stress", value: 55, weight: 0.5, unit: "idx" },
  ],
};

const riskTone = {
  Critical: "critical",
  High: "high",
  Moderate: "moderate",
  Low: "low",
};

function MetricCard({ label, value, hint }) {
  return (
    <div className="metric-card">
      <p>{label}</p>
      <h3>{value}</h3>
      <span>{hint}</span>
    </div>
  );
}

function AssessmentCard({ item }) {
  return (
    <article className="assessment-card">
      <div className="assessment-topline">
        <div>
          <p className="eyebrow">{item.region}</p>
          <h3>{item.hazard_type} Assessment</h3>
        </div>
        <span className={`risk-pill ${riskTone[item.risk_level]}`}>{item.risk_level}</span>
      </div>
      <div className="score-row">
        <div>
          <strong>{item.overall_risk_score}</strong>
          <span>Risk score</span>
        </div>
        <div>
          <strong>{item.impact_score}</strong>
          <span>Impact score</span>
        </div>
      </div>
      <p className="summary">{item.ai_summary}</p>
      <div className="breakdown-grid">
        <div>Population: {item.impact_breakdown.population_risk}</div>
        <div>Infrastructure: {item.impact_breakdown.infrastructure_risk}</div>
        <div>Environment: {item.impact_breakdown.environmental_risk}</div>
        <div>Economic: {item.impact_breakdown.economic_risk}</div>
      </div>
      <ul className="action-list">
        {item.recommended_actions.slice(0, 3).map((action) => (
          <li key={action}>{action}</li>
        ))}
      </ul>
    </article>
  );
}

function IncidentList({ incidents }) {
  return (
    <div className="incident-list">
      {incidents.map((incident) => (
        <div className="incident-item" key={incident.id}>
          <div>
            <p className="eyebrow">{incident.status}</p>
            <h4>{incident.title}</h4>
            <span>
              {incident.region} | {incident.hazard_type}
            </span>
          </div>
          <div className="incident-meta">
            <strong>{incident.severity}</strong>
            <span>{incident.affected_population.toLocaleString()} affected</span>
          </div>
        </div>
      ))}
    </div>
  );
}

function MapPreview({ region, hazardType }) {
  const query = region?.trim() ? `${region} ${hazardType}` : "India climate risk";
  const mapUrl = `https://www.google.com/maps?q=${encodeURIComponent(query)}&output=embed`;

  return (
    <section className="panel map-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Location context</p>
          <h2>Map Preview</h2>
        </div>
      </div>
      <div className="map-frame-shell">
        <iframe
          title="Location map preview"
          src={mapUrl}
          loading="lazy"
          referrerPolicy="no-referrer-when-downgrade"
        />
      </div>
      <p className="map-caption">
        {region?.trim()
          ? `Showing map context for ${region} and the selected ${hazardType.toLowerCase()} hazard.`
          : "Enter a place in the assessment form to preview its location on the map."}
      </p>
    </section>
  );
}

function App() {
  const [dashboard, setDashboard] = useState(null);
  const [form, setForm] = useState(initialForm);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function loadDashboard() {
    try {
      setError("");
      const data = await fetchDashboard();
      setDashboard(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  function updateIndicator(index, field, value) {
    setForm((current) => ({
      ...current,
      indicators: current.indicators.map((indicator, itemIndex) =>
        itemIndex === index ? { ...indicator, [field]: value } : indicator
      ),
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      await createAssessment({
        ...form,
        event_severity: Number(form.event_severity),
        exposure_index: Number(form.exposure_index),
        vulnerability_index: Number(form.vulnerability_index),
        preparedness_index: Number(form.preparedness_index),
        indicators: form.indicators.map((indicator) => ({
          ...indicator,
          value: Number(indicator.value),
          weight: Number(indicator.weight),
        })),
      });
      await loadDashboard();
      setForm({ ...initialForm, region: "" });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero-copy">
          <p className="eyebrow">AI-enabled climate intelligence</p>
          <h1>Climate Risk and Disaster Impact Assessment Platform</h1>
          <p>
            Monitor hazard exposure, assess vulnerability, and generate rapid response recommendations
            for disaster planning teams.
          </p>
        </div>
        <div className="hero-panel">
          <span>Decision Support</span>
          <strong>Preparedness + impact scoring</strong>
          <p>Built for quick demos, extension, and integration with ML or geospatial data later.</p>
        </div>
      </header>

      {error ? <div className="error-banner">{error}</div> : null}

      <main className="content-grid">
        <section className="panel metrics-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Operational overview</p>
              <h2>Dashboard</h2>
            </div>
          </div>
          <div className="metric-grid">
            <MetricCard
              label="Assessments"
              value={dashboard?.total_assessments ?? "--"}
              hint="Stored impact evaluations"
            />
            <MetricCard
              label="High Risk Regions"
              value={dashboard?.high_risk_regions ?? "--"}
              hint="High and critical cases"
            />
            <MetricCard
              label="Active Incidents"
              value={dashboard?.active_incidents ?? "--"}
              hint="Live response watchlist"
            />
            <MetricCard
              label="Average Risk"
              value={dashboard?.average_risk_score ?? "--"}
              hint="Portfolio-wide score"
            />
          </div>
        </section>

        <section className="panel form-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">New analysis</p>
              <h2>Create Assessment</h2>
            </div>
          </div>
          <form className="assessment-form" onSubmit={handleSubmit}>
            <label>
              Region
              <input
                required
                value={form.region}
                onChange={(event) => updateField("region", event.target.value)}
                placeholder="e.g. Kerala"
              />
            </label>
            <label>
              Hazard Type
              <select value={form.hazard_type} onChange={(event) => updateField("hazard_type", event.target.value)}>
                <option>Flood</option>
                <option>Cyclone</option>
                <option>Heatwave</option>
                <option>Wildfire</option>
                <option>Drought</option>
              </select>
            </label>
            <label>
              Event Severity (0-10)
              <input
                type="number"
                min="0"
                max="10"
                step="0.1"
                value={form.event_severity}
                onChange={(event) => updateField("event_severity", event.target.value)}
              />
            </label>
            <label>
              Exposure Index (0-1)
              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={form.exposure_index}
                onChange={(event) => updateField("exposure_index", event.target.value)}
              />
            </label>
            <label>
              Vulnerability Index (0-1)
              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={form.vulnerability_index}
                onChange={(event) => updateField("vulnerability_index", event.target.value)}
              />
            </label>
            <label>
              Preparedness Index (0-1)
              <input
                type="number"
                min="0"
                max="1"
                step="0.01"
                value={form.preparedness_index}
                onChange={(event) => updateField("preparedness_index", event.target.value)}
              />
            </label>

            <div className="indicator-group">
              <p className="eyebrow">Climate indicators</p>
              {form.indicators.map((indicator, index) => (
                <div className="indicator-row" key={`${indicator.name}-${index}`}>
                  <input
                    value={indicator.name}
                    onChange={(event) => updateIndicator(index, "name", event.target.value)}
                  />
                  <input
                    type="number"
                    value={indicator.value}
                    onChange={(event) => updateIndicator(index, "value", event.target.value)}
                  />
                  <input
                    type="number"
                    min="0"
                    max="1"
                    step="0.05"
                    value={indicator.weight}
                    onChange={(event) => updateIndicator(index, "weight", event.target.value)}
                  />
                  <input
                    value={indicator.unit}
                    onChange={(event) => updateIndicator(index, "unit", event.target.value)}
                  />
                </div>
              ))}
            </div>

            <button type="submit" disabled={submitting}>
              {submitting ? "Assessing..." : "Run AI Assessment"}
            </button>
          </form>
        </section>

        <MapPreview region={form.region} hazardType={form.hazard_type} />

        <section className="panel assessments-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Latest outputs</p>
              <h2>Risk Assessments</h2>
            </div>
          </div>
          <div className="assessment-list">
            {dashboard?.latest_assessments?.map((item) => <AssessmentCard key={item.id} item={item} />)}
          </div>
        </section>

        <section className="panel incidents-panel">
          <div className="section-heading">
            <div>
              <p className="eyebrow">Field monitoring</p>
              <h2>Incident Watch</h2>
            </div>
          </div>
          <IncidentList incidents={dashboard?.incidents ?? []} />
        </section>
      </main>
    </div>
  );
}

export default App;
