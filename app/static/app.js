const CANDIDATE_ID = 1;

const state = {
  jobs: [],
  intelligence: null
};

const $ = (selector) => document.querySelector(selector);

async function api(path, options = {}) {
  const response = await fetch(path, options);

  if (!response.ok) {
    let message = `Request failed (${response.status})`;

    try {
      const errorData = await response.json();

      if (errorData.detail) {
        message = errorData.detail;
      }
    } catch {
      // Keep the default error message.
    }

    throw new Error(message);
  }

  return response.json();
}

function escapeHtml(value = "") {
  return String(value).replace(
    /[&<>'"]/g,
    (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      "'": "&#39;",
      '"': "&quot;"
    })[character]
  );
}

function showToast(message) {
  const toast = $("#toast");

  if (!toast) {
    return;
  }

  toast.textContent = message;
  toast.classList.add("show");

  window.setTimeout(() => {
    toast.classList.remove("show");
  }, 2800);
}

function setLoading(selector, message = "Loading...") {
  const target = $(selector);

  if (!target) {
    return;
  }

  target.innerHTML = `
    <div class="empty-state">
      ${escapeHtml(message)}
    </div>
  `;
}

function setError(selector, message) {
  const target = $(selector);

  if (!target) {
    return;
  }

  target.innerHTML = `
    <div class="empty-state">
      ${escapeHtml(message)}
    </div>
  `;
}

function formatScore(value) {
  const score = Number(value);

  if (!Number.isFinite(score)) {
    return "—";
  }

  return `${Math.round(score)}%`;
}

function formatStatus(status) {
  return status || "Not Applied";
}


/* ---------------------------------------------------------
   OVERVIEW STATISTICS
--------------------------------------------------------- */

function updateReadyToApplyCount() {
  const target = $("#stat-ready");

  if (!target) {
    return;
  }

  const matches =
    state.intelligence?.job_matches || [];

  const readyJobs = matches.filter((job) => {
    const category =
      job.match_category || "";

    return (
      category === "Strong Match" ||
      category === "Excellent Match"
    );
  });

  target.textContent =
    readyJobs.length;
}


/* ---------------------------------------------------------
   APPLICATION ANALYTICS
--------------------------------------------------------- */

function renderApplicationAnalytics(stats) {
  const notApplied =
    Number(stats.not_applied) || 0;

  const applied =
    Number(stats.applied) || 0;

  const interview =
    Number(stats.interview) || 0;

  const rejected =
    Number(stats.rejected) || 0;

  const offer =
    Number(stats.offer) || 0;


  /* Main analytics cards */

  const analyticsNotApplied =
    $("#analytics-not-applied");

  if (analyticsNotApplied) {
    analyticsNotApplied.textContent =
      notApplied;
  }


  const analyticsApplied =
    $("#analytics-applied");

  if (analyticsApplied) {
    analyticsApplied.textContent =
      applied;
  }


  const analyticsInterview =
    $("#analytics-interview");

  if (analyticsInterview) {
    analyticsInterview.textContent =
      interview;
  }


  const analyticsOffer =
    $("#analytics-offer");

  if (analyticsOffer) {
    analyticsOffer.textContent =
      offer;
  }


  /* Funnel */

  const funnelNotApplied =
    $("#funnel-not-applied");

  if (funnelNotApplied) {
    funnelNotApplied.textContent =
      notApplied;
  }


  const funnelApplied =
    $("#funnel-applied");

  if (funnelApplied) {
    funnelApplied.textContent =
      applied;
  }


  const funnelInterview =
    $("#funnel-interview");

  if (funnelInterview) {
    funnelInterview.textContent =
      interview;
  }


  const funnelOffer =
    $("#funnel-offer");

  if (funnelOffer) {
    funnelOffer.textContent =
      offer;
  }


  /* Pipeline summary */

  const rejectedTarget =
    $("#analytics-rejected");

  if (rejectedTarget) {
    rejectedTarget.textContent =
      rejected;
  }


  const totalAppliedTarget =
    $("#analytics-total-applied");

  if (totalAppliedTarget) {
    totalAppliedTarget.textContent =
      applied;
  }


  /*
    Interview conversion:
    interviews / applications
  */

  const interviewRate =
    applied > 0
      ? (interview / applied) * 100
      : 0;

  const interviewRateTarget =
    $("#analytics-interview-rate");

  if (interviewRateTarget) {
    interviewRateTarget.textContent =
      `${Math.round(interviewRate)}%`;
  }


  /*
    Offer conversion:
    offers / applications
  */

  const offerRate =
    applied > 0
      ? (offer / applied) * 100
      : 0;

  const offerRateTarget =
    $("#analytics-offer-rate");

  if (offerRateTarget) {
    offerRateTarget.textContent =
      `${Math.round(offerRate)}%`;
  }


  renderAnalyticsInsight({
    notApplied,
    applied,
    interview,
    rejected,
    offer,
    interviewRate,
    offerRate
  });
}


function renderAnalyticsInsight(data) {
  const target =
    $("#analytics-insight");

  if (!target) {
    return;
  }

  const {
    notApplied,
    applied,
    interview,
    rejected,
    offer,
    interviewRate,
    offerRate
  } = data;


  const totalTracked =
    notApplied +
    applied +
    interview +
    rejected +
    offer;


  let headline = "";
  let message = "";


  if (offer > 0) {
    headline =
      "Your pipeline is producing results.";

    message =
      `You currently have ${offer} offer${offer === 1 ? "" : "s"
      }. Keep prioritising the strongest job matches while maintaining your active interview pipeline.`;

  } else if (interview > 0) {
    headline =
      "Your applications are reaching the interview stage.";

    message =
      `You currently have ${interview} active interview${interview === 1 ? "" : "s"
      }. Focus on interview preparation and continue applying to strong matches so your pipeline stays healthy.`;

  } else if (applied > 0) {
    headline =
      "Your application pipeline has started.";

    message =
      `You have ${applied} application${applied === 1 ? "" : "s"
      } and no active interviews yet. Use your strongest matches first and tailor applications toward the required skills.`;

  } else {
    headline =
      "Your application pipeline is ready to start.";

    message =
      `You have ${notApplied} opportunities that have not been applied to yet. Start with the strongest AI-ranked matches rather than applying randomly.`;
  }


  let conversionMessage = "";

  if (applied > 0) {
    conversionMessage =
      ` Your current interview conversion is ${Math.round(
        interviewRate
      )}% and offer conversion is ${Math.round(
        offerRate
      )}%.`;
  }


  let rejectionMessage = "";

  if (rejected > 0) {
    rejectionMessage =
      ` You have ${rejected} rejected application${rejected === 1 ? "" : "s"
      }, so reviewing application targeting and skill gaps may help.`;
  }


  target.innerHTML = `
    <div class="analytics-insight">

      <h4>
        ${escapeHtml(headline)}
      </h4>

      <p>
        ${escapeHtml(
    message +
    conversionMessage +
    rejectionMessage
  )}
      </p>

      <small>
        Based on ${totalTracked} tracked application
        pipeline record${totalTracked === 1 ? "" : "s"
    }.
      </small>

    </div>
  `;
}


/* ---------------------------------------------------------
   NAVIGATION
--------------------------------------------------------- */

const pageTitles = {
  overview: "Your career command center",
  jobs: "Explore opportunities",
  insights: "Personalised career insights",
  market: "Market skill signals",
  analytics: "Application analytics"
};

function showSection(section) {
  if (!pageTitles[section]) {
    section = "overview";
  }

  document
    .querySelectorAll(".page-section")
    .forEach((item) => {
      item.classList.toggle(
        "active",
        item.id === section
      );
    });

  document
    .querySelectorAll(".nav-link")
    .forEach((item) => {
      item.classList.toggle(
        "active",
        item.dataset.section === section
      );
    });

  const pageTitle =
    $("#page-title");

  if (pageTitle) {
    pageTitle.textContent =
      pageTitles[section];
  }

  if (
    window.location.hash !==
    `#${section}`
  ) {
    window.history.replaceState(
      null,
      "",
      `#${section}`
    );
  }
}

document
  .querySelectorAll(
    ".nav-link, [data-go]"
  )
  .forEach((link) => {
    link.addEventListener(
      "click",
      (event) => {
        const section =
          link.dataset.section ||
          link.dataset.go;

        if (!section) {
          return;
        }

        event.preventDefault();
        showSection(section);
      }
    );
  });

window.addEventListener(
  "hashchange",
  () => {
    showSection(
      window.location.hash.replace(
        "#",
        ""
      ) ||
      "overview"
    );
  }
);


/* ---------------------------------------------------------
   JOBS
--------------------------------------------------------- */

function renderJobs(jobs) {
  const target =
    $("#job-list");

  if (!target) {
    return;
  }

  if (!jobs || !jobs.length) {
    target.innerHTML = `
      <div class="empty-state">
        No jobs match those filters.
      </div>
    `;
    return;
  }

  target.innerHTML = jobs
    .map(
      (job) => `
        <article class="job-card">

          <span class="tag ${job.application_status ===
          "Interview"
          ? "warn"
          : ""
        }">
            ${escapeHtml(
          formatStatus(
            job.application_status
          )
        )}
          </span>

          <h3>
            ${escapeHtml(job.title)}
          </h3>

          <p>
            ${escapeHtml(job.company)}
            ·
            ${escapeHtml(job.location)}
          </p>

          <div class="job-meta">

            <span>
              ${escapeHtml(
          job.salary ||
          (
            job.salary_lpa != null
              ? `${job.salary_lpa} LPA`
              : "Salary not listed"
          )
        )}
            </span>

            <span>
              ${job.extracted_skills
          ?.length || 0
        }
              skills
            </span>

          </div>

          ${job.source_url
          ? `
                <a
                  class="job-link"
                  href="${escapeHtml(
            job.source_url
          )}"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  View original job →
                </a>
              `
          : ""
        }

          <label
            class="sr-only"
            for="status-${job.job_id}"
          >
            Application status for
            ${escapeHtml(job.title)}
          </label>

          <select
            id="status-${job.job_id}"
            data-job-id="${job.job_id}"
            class="status-select"
          >

            ${[
          "Not Applied",
          "Applied",
          "Interview",
          "Rejected",
          "Offer"
        ]
          .map(
            (status) => `
                  <option
                    value="${status}"
                    ${status ===
                formatStatus(
                  job.application_status
                )
                ? "selected"
                : ""
              }
                  >
                    ${status}
                  </option>
                `
          )
          .join("")}

          </select>

          <label
            class="sr-only"
            for="notes-${job.job_id}"
          >
            Application notes for
            ${escapeHtml(job.title)}
          </label>

          <textarea
            id="notes-${job.job_id}"
            class="notes-input"
            data-job-id="${job.job_id}"
            rows="3"
            maxlength="2000"
            placeholder="Application notes..."
          >${escapeHtml(
            job.application_notes || ""
          )}</textarea>

          <button
            type="button"
            class="secondary-button notes-button"
            data-job-id="${job.job_id}"
          >
            Save notes
          </button>

        </article>
      `
    )
    .join("");


  document
    .querySelectorAll(
      ".status-select"
    )
    .forEach((select) => {
      select.addEventListener(
        "change",
        updateStatus
      );
    });


  document
    .querySelectorAll(
      ".notes-button"
    )
    .forEach((button) => {
      button.addEventListener(
        "click",
        updateNotes
      );
    });
}


async function updateStatus(event) {
  const select =
    event.target;

  const jobId =
    select.dataset.jobId;

  const newStatus =
    select.value;

  select.disabled = true;

  try {
    await api(
      `/jobs/${jobId}/application-status`,
      {
        method: "PUT",
        headers: {
          "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
          status: newStatus
        })
      }
    );


    const job =
      state.jobs.find(
        (item) =>
          item.job_id ===
          Number(jobId)
      );


    if (job) {
      job.application_status =
        newStatus;
    }


    showToast(
      "Application status updated"
    );


    await loadStatistics();
    await loadIntelligence();

  } catch (error) {

    showToast(
      error.message ||
      "Could not update application status"
    );

    await loadJobs();

  } finally {
    select.disabled = false;
  }
}


async function updateNotes(event) {
  const button =
    event.target;

  const jobId =
    button.dataset.jobId;

  const textarea =
    $(`#notes-${jobId}`);

  if (!textarea) {
    return;
  }

  button.disabled = true;

  try {
    await api(
      `/jobs/${jobId}/application-notes`,
      {
        method: "PUT",
        headers: {
          "Content-Type":
            "application/json"
        },
        body: JSON.stringify({
          notes:
            textarea.value
        })
      }
    );


    const job =
      state.jobs.find(
        (item) =>
          item.job_id ===
          Number(jobId)
      );


    if (job) {
      job.application_notes =
        textarea.value;
    }


    showToast(
      "Application notes saved"
    );

  } catch (error) {

    showToast(
      error.message ||
      "Could not save application notes"
    );

  } finally {
    button.disabled = false;
  }
}


async function loadJobs(query = "") {
  setLoading(
    "#job-list",
    "Loading job opportunities..."
  );

  try {
    const endpoint =
      query
        ? `/jobs/search${query}`
        : "/jobs";

    state.jobs =
      await api(endpoint);

    renderJobs(
      state.jobs
    );


    const statJobs =
      $("#stat-jobs");

    if (statJobs) {
      statJobs.textContent =
        state.jobs.length;
    }

  } catch (error) {

    setError(
      "#job-list",
      "Jobs could not be loaded. Check the API server."
    );


    const statJobs =
      $("#stat-jobs");

    if (statJobs) {
      statJobs.textContent =
        "—";
    }


    showToast(
      error.message ||
      "Could not load jobs"
    );
  }
}


/* ---------------------------------------------------------
   CANDIDATE INTELLIGENCE
--------------------------------------------------------- */

function renderIntelligence(data) {
  state.intelligence =
    data;


  const profile =
    data.profile || {};


  const candidateName =
    $("#candidate-name");

  if (candidateName) {
    candidateName.textContent =
      profile.name ||
      "Candidate profile";
  }


  const candidateMeta =
    $("#candidate-meta");

  if (candidateMeta) {
    candidateMeta.textContent =
      `${profile.education ||
      "Career profile"
      } · ${profile.experience_years ??
      0
      } years experience`;
  }


  const readiness =
    data.candidate_readiness ||
    {};


  const readinessStat =
    $("#stat-readiness");

  if (readinessStat) {
    readinessStat.textContent =
      readiness.readiness_score != null
        ? formatScore(
          readiness.readiness_score
        )
        : "—";
  }


  updateReadyToApplyCount();


  const matches =
    data.job_matches ||
    data.saved_matches ||
    [];


  renderTopMatches(
    matches
  );


  renderTopSkills(
    data.skill_priorities ||
    []
  );


  renderRecommendations(
    data.recommendations ||
    []
  );


  renderSkillGaps(
    data.skill_gaps ||
    []
  );


  renderCareerAdvice(
    data
  );
}


function renderTopMatches(matches) {
  const target =
    $("#top-matches");

  if (!target) {
    return;
  }


  if (!matches.length) {
    target.innerHTML = `
      <div class="empty-state">
        No job matches available yet.
      </div>
    `;
    return;
  }


  target.innerHTML =
    matches
      .slice(0, 5)
      .map((match) => {

        const score =
          match.combined_match ??
          match.overall_match ??
          0;


        return `
          <div class="match-row">

            <div>

              <div class="match-title">
                ${escapeHtml(
          match.title
        )}
              </div>

              <div class="match-subtitle">
                ${escapeHtml(
          match.company
        )}
                ·
                ${escapeHtml(
          match.match_category ||
          "Potential match"
        )}
              </div>

            </div>

            <div class="score">
              ${formatScore(
          score
        )}
            </div>

          </div>
        `;
      })
      .join("");
}


function renderTopSkills(priorities) {
  const target =
    $("#top-skills");

  if (!target) {
    return;
  }


  if (!priorities.length) {
    target.innerHTML = `
      <div class="empty-state">
        No skill priorities available yet.
      </div>
    `;
    return;
  }


  target.innerHTML =
    priorities
      .slice(0, 6)
      .map(
        (skill) => `
          <div class="skill-row">

            <span>
              ${escapeHtml(
          skill.skill
        )}
            </span>

            <span class="skill-chip">
              ${escapeHtml(
          skill.priority_category ||
          "Priority"
        )}
            </span>

          </div>
        `
      )
      .join("");
}


function renderRecommendations(
  recommendations
) {
  const target =
    $("#recommendations");

  if (!target) {
    return;
  }


  if (!recommendations.length) {
    target.innerHTML = `
      <div class="empty-state">
        No recommendations available yet.
      </div>
    `;
    return;
  }


  target.innerHTML =
    recommendations
      .slice(0, 6)
      .map(
        (item) => `
          <div class="recommendation-row">

            <div>

              <div class="match-title">
                ${escapeHtml(
          item.title
        )}
              </div>

              <div class="match-subtitle">
                ${escapeHtml(
          item.company
        )}
                ·
                ${escapeHtml(
          item.recommendation ||
          "Potential opportunity"
        )}
              </div>

            </div>

            <div class="score">
              ${formatScore(
          item.overall_match
        )}
            </div>

          </div>
        `
      )
      .join("");
}


function renderSkillGaps(
  skillGaps
) {
  const target =
    $("#skill-gaps");

  if (!target) {
    return;
  }


  if (!skillGaps.length) {
    target.innerHTML = `
      <div class="empty-state">
        No skill gaps found.
      </div>
    `;
    return;
  }


  target.innerHTML =
    skillGaps
      .slice(0, 8)
      .map(
        (skill) => `
          <div class="skill-row">

            <span>
              ${escapeHtml(
          skill.skill
        )}
            </span>

            <span class="skill-chip">
              ${skill.opportunity_count ||
          0
          }
              jobs
            </span>

          </div>
        `
      )
      .join("");
}


function renderCareerAdvice(
  data
) {
  const target =
    $("#career-advice");

  if (!target) {
    return;
  }


  const advice =
    data.career_advice ||
    {};


  const actions =
    data.career_action_plan ||
    advice.priority_actions ||
    [];


  if (!actions.length) {
    target.innerHTML = `
      <p>
        Your profile is ready. Keep building
        relevant skills and applying to the
        strongest matches.
      </p>
    `;
    return;
  }


  target.innerHTML = `
    <ul>
      ${actions
      .slice(0, 6)
      .map((action) => {

        const text =
          typeof action ===
            "string"
            ? action
            : action.action ||
            action.description ||
            action.skill ||
            "Focus on your next priority skill.";


        return `
            <li>
              ${escapeHtml(text)}
            </li>
          `;
      })
      .join("")}
    </ul>
  `;
}


async function loadIntelligence() {
  [
    "#top-matches",
    "#top-skills",
    "#recommendations",
    "#skill-gaps",
    "#career-advice"
  ].forEach((selector) => {
    setLoading(
      selector,
      "Building career intelligence..."
    );
  });


  try {

    const intelligence =
      await api(
        `/candidates/${CANDIDATE_ID}/intelligence`
      );


    renderIntelligence(
      intelligence
    );

  } catch (error) {

    [
      "#top-matches",
      "#top-skills",
      "#recommendations",
      "#skill-gaps",
      "#career-advice"
    ].forEach((selector) => {

      setError(
        selector,
        "Career intelligence could not be loaded."
      );

    });


    showToast(
      error.message ||
      "Could not load career intelligence"
    );
  }
}


/* ---------------------------------------------------------
   APPLICATION STATISTICS
--------------------------------------------------------- */

async function loadStatistics() {
  try {

    const stats =
      await api(
        "/applications/statistics"
      );


    /*
      Overview cards
    */

    const interviewStat =
      $("#stat-interview");

    if (interviewStat) {
      interviewStat.textContent =
        stats.interview ?? 0;
    }


    /*
      Ready to apply comes from
      candidate intelligence.
    */

    updateReadyToApplyCount();


    /*
      Full analytics section
    */

    renderApplicationAnalytics(
      stats
    );

  } catch (error) {

    const interviewStat =
      $("#stat-interview");

    if (interviewStat) {
      interviewStat.textContent =
        "—";
    }


    if (!state.intelligence) {

      const readyStat =
        $("#stat-ready");

      if (readyStat) {
        readyStat.textContent =
          "—";
      }

    }


    [
      "#analytics-not-applied",
      "#analytics-applied",
      "#analytics-interview",
      "#analytics-offer",
      "#analytics-rejected",
      "#analytics-total-applied",
      "#analytics-interview-rate",
      "#analytics-offer-rate",
      "#funnel-not-applied",
      "#funnel-applied",
      "#funnel-interview",
      "#funnel-offer"
    ].forEach((selector) => {

      const target =
        $(selector);

      if (target) {
        target.textContent =
          "—";
      }

    });


    setError(
      "#analytics-insight",
      "Application analytics could not be loaded."
    );


    showToast(
      error.message ||
      "Could not load application statistics"
    );
  }
}


/* ---------------------------------------------------------
   MARKET SKILLS
--------------------------------------------------------- */

async function loadMarket() {
  const target =
    $("#market-skills");

  if (!target) {
    return;
  }


  setLoading(
    "#market-skills",
    "Loading market demand..."
  );


  try {

    const skills =
      await api(
        "/market/skills"
      );


    if (!skills.length) {

      target.innerHTML = `
        <div class="empty-state">
          No market skill data available.
        </div>
      `;

      return;
    }


    target.innerHTML = `
      <table>

        <thead>

          <tr>
            <th>SKILL</th>
            <th>JOBS</th>
            <th>REQUIRED</th>
            <th>DEMAND</th>
          </tr>

        </thead>

        <tbody>

          ${skills
        .map(
          (item) => `
                <tr>

                  <td>
                    <strong>
                      ${escapeHtml(
            item.skill
          )}
                    </strong>
                  </td>

                  <td>
                    ${item.job_count ??
            0
            }
                  </td>

                  <td>
                    ${item.required_count ??
            0
            }
                  </td>

                  <td>

                    <div class="bar">

                      <span
                        style="width:${Math.min(
              100,
              Number(
                item.demand_percentage
              ) || 0
            )}%"
                      ></span>

                    </div>

                    ${Number(
              item.demand_percentage
            ) || 0
            }%

                  </td>

                </tr>
              `
        )
        .join("")}

        </tbody>

      </table>
    `;

  } catch (error) {

    setError(
      "#market-skills",
      "Market skill data could not be loaded."
    );


    showToast(
      error.message ||
      "Could not load market data"
    );
  }
}


/* ---------------------------------------------------------
   API HEALTH
--------------------------------------------------------- */

async function checkHealth() {
  try {

    await api("/health");


    const apiStatus =
      $("#api-status");

    if (!apiStatus) {
      return;
    }


    apiStatus.classList.remove(
      "offline"
    );


    apiStatus.innerHTML = `
      <i></i>
      <span>API connected</span>
    `;

  } catch {

    const apiStatus =
      $("#api-status");

    if (!apiStatus) {
      return;
    }


    apiStatus.classList.add(
      "offline"
    );


    apiStatus.innerHTML = `
      <i></i>
      <span>API offline</span>
    `;
  }
}


/* ---------------------------------------------------------
   JOB SEARCH
--------------------------------------------------------- */

const jobSearch =
  $("#job-search");

if (jobSearch) {

  jobSearch.addEventListener(
    "submit",
    (event) => {

      event.preventDefault();


      const params =
        new URLSearchParams();


      const title =
        $("#search-title")
          ?.value
          .trim();


      const location =
        $("#search-location")
          ?.value
          .trim();


      const salary =
        $("#search-salary")
          ?.value;


      if (title) {
        params.set(
          "title",
          title
        );
      }


      if (location) {
        params.set(
          "location",
          location
        );
      }


      if (salary) {
        params.set(
          "minimum_salary",
          salary
        );
      }


      const query =
        params.toString()
          ? `?${params.toString()}`
          : "";


      loadJobs(query);
    }
  );
}


const clearSearch =
  $("#clear-search");

if (clearSearch) {

  clearSearch.addEventListener(
    "click",
    () => {

      $("#job-search")
        ?.reset();

      loadJobs();
    }
  );
}


/* ---------------------------------------------------------
   REFRESH BUTTONS
--------------------------------------------------------- */

const refreshIntelligence =
  $("#refresh-intelligence");

if (refreshIntelligence) {

  refreshIntelligence.addEventListener(
    "click",
    async () => {

      const button =
        $("#refresh-intelligence");


      button.disabled = true;

      button.textContent =
        "Refreshing...";


      try {

        await Promise.all([
          loadIntelligence(),
          loadStatistics(),
          loadJobs(),
          loadMarket()
        ]);


        showToast(
          "Career intelligence refreshed"
        );

      } finally {

        button.disabled = false;

        button.textContent =
          "Refresh insights";
      }
    }
  );
}


const reloadInsights =
  $("#reload-insights");

if (reloadInsights) {

  reloadInsights.addEventListener(
    "click",
    async () => {

      const button =
        $("#reload-insights");


      button.disabled = true;

      button.textContent =
        "Refreshing...";


      try {

        await loadIntelligence();


        showToast(
          "Career insights refreshed"
        );

      } finally {

        button.disabled = false;

        button.textContent =
          "Refresh insights";
      }
    }
  );
}


/* ---------------------------------------------------------
   INITIAL LOAD
--------------------------------------------------------- */

showSection(
  window.location.hash.replace(
    "#",
    ""
  ) ||
  "overview"
);

checkHealth();
loadJobs();
loadStatistics();
loadMarket();
loadIntelligence();