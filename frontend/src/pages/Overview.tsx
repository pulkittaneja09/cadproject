import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { OverviewAnalytics } from "../types";
import { apiClient } from "../lib/api";
import { Card } from "../components/ui/Card";
import LoadingSpinner from "../components/ui/LoadingSpinner";
import {
  ArrowUpRight,
  ArrowRight,
  MessageSquare,
  Smile,
  Meh,
  Frown,
  Flag,
  RefreshCw,
  AudioLines,
  Sparkles,
} from "lucide-react";
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  BarChart,
  Bar,
} from "recharts";
interface Props {
  selectedDataset: number | null;
  refreshDatasets: () => void;
}
const colors = { positive: "#65c9ab", neutral: "#d6b773", negative: "#e18f9d" };
export default function Overview({ selectedDataset }: Props) {
  const [data, setData] = useState<OverviewAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [revision, setRevision] = useState(0);
  const [trend, setTrend] = useState<"sentiment" | "volume">("sentiment");
  const [updated, setUpdated] = useState("");
  useEffect(() => {
    let active = true;
    setLoading(true);
    apiClient
      .getOverviewAnalytics(selectedDataset ?? undefined)
      .then((r) => {
        if (active) {
          setData(r.data);
          setError(false);
          setUpdated(
            new Date().toLocaleTimeString(undefined, {
              hour: "2-digit",
              minute: "2-digit",
            }),
          );
        }
      })
      .catch(() => {
        if (active) setError(true);
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, [selectedDataset, revision]);
  if (loading)
    return (
      <div className="loading-state" role="status">
        <LoadingSpinner />
        <p>Reading the room…</p>
      </div>
    );
  if (error || !data)
    return (
      <div className="empty-state">
        <AudioLines size={36} />
        <h2>Your overview is unavailable</h2>
        <p>Check the backend connection, then try again.</p>
        <button
          className="import-link"
          onClick={() => setRevision((r) => r + 1)}
        >
          Try again
        </button>
      </div>
    );
  const analyzed = Object.values(data.sentiment_distribution).reduce(
    (a, b) => a + b,
    0,
  );
  const metrics = [
    {
      label: "Total feedback",
      value: data.kpi.total_reviews.toLocaleString(),
      detail: `${analyzed.toLocaleString()} analyzed reviews`,
      icon: MessageSquare,
      tone: "",
    },
    {
      label: "Positive sentiment",
      value: `${data.kpi.positive_percentage}%`,
      detail: `${data.sentiment_distribution.positive} positive reviews`,
      icon: Smile,
      tone: "positive",
    },
    {
      label: "Neutral sentiment",
      value: `${data.kpi.neutral_percentage}%`,
      detail: `${data.sentiment_distribution.neutral} neutral reviews`,
      icon: Meh,
      tone: "neutral",
    },
    {
      label: "Negative sentiment",
      value: `${data.kpi.negative_percentage}%`,
      detail: `${data.sentiment_distribution.negative} negative reviews`,
      icon: Frown,
      tone: "negative",
    },
  ];
  return (
    <div className="overview">
      <div className="scope-bar">
        <div>
          <span className="scope-dot" />{" "}
          {selectedDataset ? "Selected dataset" : "All customer feedback"}
          <span className="scope-divider" />
          All time
        </div>
        <button
          onClick={() => setRevision((r) => r + 1)}
          className="refresh-button"
        >
          <RefreshCw size={13} />
          Updated {updated}
        </button>
      </div>
      {data.kpi.total_reviews === 0 ? (
        <div className="welcome-panel">
          <AudioLines size={40} />
          <h2>Your customers have a story to tell.</h2>
          <p>
            Import a feedback CSV and run analysis to uncover sentiment,
            recurring issues, and the voices that need attention.
          </p>
          <Link className="import-link" to="/import">
            Import your first dataset
            <ArrowRight size={16} />
          </Link>
        </div>
      ) : null}
      <section className="metrics" aria-label="Feedback summary">
        {metrics.map(({ label, value, detail, icon: Icon, tone }) => (
          <div className={`metric ${tone}`} key={label}>
            <div className="metric-label">
              {label}
              <Icon size={17} />
            </div>
            <strong>{value}</strong>
            <small>{detail}</small>
          </div>
        ))}
      </section>
      <div className="analysis-grid">
        <Card className="trend-panel">
          <div className="panel-heading">
            <div>
              <h2>
                {trend === "sentiment"
                  ? "Sentiment over time"
                  : "Feedback volume"}
              </h2>
              <p>
                {trend === "sentiment"
                  ? "How customer perception is evolving"
                  : "The rhythm of your customer conversations"}
              </p>
            </div>
            <div className="segmented" aria-label="Chart view">
              <button
                aria-pressed={trend === "sentiment"}
                onClick={() => setTrend("sentiment")}
              >
                Sentiment
              </button>
              <button
                aria-pressed={trend === "volume"}
                onClick={() => setTrend("volume")}
              >
                Volume
              </button>
            </div>
          </div>
          {data.sentiment_trends.length ? (
            <>
              <div className="chart-legend">
                {trend === "sentiment" ? (
                  Object.entries(colors).map(([name, color]) => (
                    <span key={name}>
                      <i style={{ background: color }} />
                      {name}
                    </span>
                  ))
                ) : (
                  <span>
                    <i style={{ background: "#a79cf5" }} />
                    Total feedback
                  </span>
                )}
              </div>
              <div
                role="img"
                aria-label="Feedback counts over time. Exact values are available in the table below."
                className="chart-wrap"
              >
                <ResponsiveContainer width="100%" height={248}>
                  <AreaChart
                    data={
                      trend === "sentiment"
                        ? data.sentiment_trends
                        : data.volume_over_time
                    }
                    margin={{ top: 15, right: 10, left: -25, bottom: 0 }}
                  >
                    <defs>
                      {Object.entries({ ...colors, count: "#a79cf5" }).map(
                        ([name, color]) => (
                          <linearGradient
                            id={`fill-${name}`}
                            key={name}
                            x1="0"
                            y1="0"
                            x2="0"
                            y2="1"
                          >
                            <stop
                              offset="0%"
                              stopColor={color}
                              stopOpacity={0.15}
                            />
                            <stop
                              offset="100%"
                              stopColor={color}
                              stopOpacity={0}
                            />
                          </linearGradient>
                        ),
                      )}
                    </defs>
                    <CartesianGrid
                      stroke="#2a2c35"
                      vertical={false}
                      strokeDasharray="3 5"
                    />
                    <XAxis
                      dataKey="date"
                      tickFormatter={(v) =>
                        new Date(v).toLocaleDateString(undefined, {
                          month: "short",
                          day: "numeric",
                        })
                      }
                      stroke="#8e919e"
                      tickLine={false}
                      axisLine={false}
                      minTickGap={28}
                      fontSize={11}
                    />
                    <YAxis
                      allowDecimals={false}
                      stroke="#8e919e"
                      tickLine={false}
                      axisLine={false}
                      fontSize={11}
                    />
                    <Tooltip
                      contentStyle={{
                        background: "#22242d",
                        border: "1px solid #3b3e4c",
                        borderRadius: 8,
                      }}
                    />
                    {Object.entries(
                      trend === "sentiment" ? colors : { count: "#a79cf5" },
                    ).map(([key, color]) => (
                      <Area
                        key={key}
                        type="monotone"
                        dataKey={key}
                        stroke={color}
                        fill={`url(#fill-${key})`}
                        strokeWidth={2}
                        isAnimationActive={false}
                      />
                    ))}
                  </AreaChart>
                </ResponsiveContainer>
              </div>
              <details className="data-details">
                <summary>View chart data</summary>
                <div className="table-scroll">
                  <table>
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Positive</th>
                        <th>Neutral</th>
                        <th>Negative</th>
                        <th>Total</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.sentiment_trends.map((r) => (
                        <tr key={r.date}>
                          <td>{r.date}</td>
                          <td>{r.positive}</td>
                          <td>{r.neutral}</td>
                          <td>{r.negative}</td>
                          <td>{r.count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </details>
            </>
          ) : (
            <div className="chart-empty">
              Dated feedback will appear here after analysis.
            </div>
          )}
        </Card>
        <Card className="mix-panel">
          <div className="panel-heading">
            <div>
              <h2>The sentiment mix</h2>
              <p>A snapshot of analyzed feedback</p>
            </div>
            <AudioLines size={18} className="text-gray-400" />
          </div>
          <div
            className="sentiment-ring"
            style={{
              background: analyzed
                ? `conic-gradient(${colors.positive} 0 ${(data.sentiment_distribution.positive / analyzed) * 100}%, ${colors.neutral} 0 ${((data.sentiment_distribution.positive + data.sentiment_distribution.neutral) / analyzed) * 100}%, ${colors.negative} 0 100%)`
                : "#30323c",
            }}
          >
            <div>
              <strong>{analyzed.toLocaleString()}</strong>
              <span>analyzed reviews</span>
            </div>
          </div>
          <div className="mix-legend">
            {Object.entries(colors).map(([name, color]) => (
              <Link to={`/feedback?sentiment=${name}`} key={name}>
                <span>
                  <i style={{ background: color }} />
                  {name}
                </span>
                <strong>
                  {data.sentiment_distribution[
                    name as keyof typeof colors
                  ].toLocaleString()}
                </strong>
                <small>
                  {analyzed
                    ? (
                        (data.sentiment_distribution[
                          name as keyof typeof colors
                        ] /
                          analyzed) *
                        100
                      ).toFixed(1)
                    : 0}
                  %
                </small>
              </Link>
            ))}
          </div>
        </Card>
      </div>
      <div className="secondary-grid">
        <Card>
          <div className="panel-heading">
            <div>
              <h2>What customers talk about</h2>
              <p>Feedback by complaint category</p>
            </div>
            <Link to="/feedback" className="text-link">
              Explore
              <ArrowUpRight size={14} />
            </Link>
          </div>
          <div className="category-list">
            {data.category_breakdown.length ? (
              data.category_breakdown.map((c, i) => (
                <Link
                  to={`/feedback?category=${encodeURIComponent(c.category)}`}
                  key={c.category}
                  className="category-row"
                >
                  <span>{c.category}</span>
                  <div className="category-track">
                    <div
                      style={{
                        width: `${c.percentage}%`,
                        background: i === 0 ? "#a79cf5" : "#666582",
                      }}
                    />
                  </div>
                  <strong>{c.count}</strong>
                  <small>{c.percentage.toFixed(0)}%</small>
                </Link>
              ))
            ) : (
              <p className="chart-empty">
                Analyze feedback to discover category patterns.
              </p>
            )}
          </div>
        </Card>
        <Card className="attention-panel">
          <div className="attention-icon">
            <Flag size={20} />
          </div>
          <h2>
            {data.kpi.high_priority_complaints
              ? "Give these voices attention."
              : "Room to listen closer."}
          </h2>
          <div className="attention-count">
            {data.kpi.high_priority_complaints}
            <span>high-priority complaints</span>
          </div>
          <p>
            Start with the feedback that needs the most care. Review each
            complaint and its priority explanation.
          </p>
          <Link
            to={
              data.kpi.high_priority_complaints
                ? "/feedback?priority=high"
                : "/feedback"
            }
            className="attention-link"
          >
            {data.kpi.high_priority_complaints
              ? "Review priority feedback"
              : "Explore customer feedback"}
            <ArrowRight size={16} />
          </Link>
        </Card>
      </div>
      {data.product_sentiment.length > 0 && (
        <Card>
          <div className="panel-heading">
            <div>
              <h2>Product pulse</h2>
              <p>Sentiment across your products</p>
            </div>
          </div>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Product</th>
                  <th>Reviews</th>
                  <th>Positive</th>
                  <th>Neutral</th>
                  <th>Negative</th>
                  <th>Positive share</th>
                </tr>
              </thead>
              <tbody>
                {data.product_sentiment.map((p) => (
                  <tr key={p.product}>
                    <td>
                      <Link
                        to={`/feedback?product=${encodeURIComponent(p.product)}`}
                      >
                        {p.product}
                      </Link>
                    </td>
                    <td>{p.total}</td>
                    <td className="text-success">{p.positive}</td>
                    <td className="text-warning">{p.neutral}</td>
                    <td className="text-danger">{p.negative}</td>
                    <td>{p.positive_percentage}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
      {data.rating_distribution.length > 0 && (
        <Card>
          <div className="panel-heading">
            <div>
              <h2>Rating distribution</h2>
              <p>Customer ratings, from one to five stars</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={data.rating_distribution}>
              <XAxis dataKey="rating" stroke="#9395a3" />
              <YAxis allowDecimals={false} stroke="#9395a3" />
              <Tooltip
                contentStyle={{
                  background: "#22242d",
                  border: "1px solid #3b3e4c",
                }}
              />
              <Bar
                dataKey="count"
                fill="#a79cf5"
                radius={[4, 4, 0, 0]}
                isAnimationActive={false}
              />
            </BarChart>
          </ResponsiveContainer>
          <div className="chart-legend">
            {data.rating_distribution.map((r) => (
              <span key={r.rating}>
                {r.rating} stars: {r.count} ({r.percentage}%)
              </span>
            ))}
          </div>
        </Card>
      )}
      <div className="insight-strip">
        <Sparkles size={20} />
        <div>
          <strong>Find the story behind the sentiment</strong>
          <p>
            Explore recurring themes and suggestions grounded in your feedback.
          </p>
        </div>
        <Link to="/insights">
          Open insights
          <ArrowUpRight size={16} />
        </Link>
      </div>
    </div>
  );
}
