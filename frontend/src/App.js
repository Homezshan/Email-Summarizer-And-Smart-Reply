import React, { useState } from 'react';
import './App.css';
import { GoogleOAuthProvider, useGoogleLogin } from '@react-oauth/google';
import { API_BASE } from "./config";

function GmailReader() {
  const [accessToken, setAccessToken] = useState(null);
  const [emails, setEmails] = useState([]);
  const [loadingIndex, setLoadingIndex] = useState(null);
  const [summaries, setSummaries] = useState({});
  const [replies, setReplies] = useState({});
  const [expandedIndex, setExpandedIndex] = useState(null);

  const login = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/gmail.readonly',
    onSuccess: tokenResponse => setAccessToken(tokenResponse.access_token),
    onError: () => alert('Login Failed'),
  });

  const fetchEmails = async () => {
    if (!accessToken) return alert('Please login first');

    try {
      const listRes = await fetch(
        'https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=5',
        { headers: { Authorization: `Bearer ${accessToken}` } }
      );

      const listData = await listRes.json();
      if (!listData.messages) return alert('No messages found');

      const emailDetails = [];

      for (const msg of listData.messages) {
        const msgRes = await fetch(
          `https://gmail.googleapis.com/gmail/v1/users/me/messages/${msg.id}`,
          { headers: { Authorization: `Bearer ${accessToken}` } }
        );

        const msgData = await msgRes.json();
        const headers = msgData.payload.headers;

        emailDetails.push({
          from: headers.find(h => h.name === 'From')?.value || 'Unknown Sender',
          subject: headers.find(h => h.name === 'Subject')?.value || 'No Subject',
          snippet: msgData.snippet,
        });
      }

      setEmails(emailDetails);
    } catch (err) {
      console.error('Failed to fetch emails:', err);
      alert('Error fetching emails');
    }
  };

  const handleSummarize = async (text, index) => {
    setLoadingIndex(index);
    try {
      const response = await fetch(`${API_BASE}/summarize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setSummaries(prev => ({ ...prev, [index]: data.summary || 'No summary generated' }));
    } catch (err) {
      console.error('Summarization failed:', err);
      alert('Error summarizing email');
    } finally {
      setLoadingIndex(null);
    }
  };

  const generateReply = async (text, index) => {
    try {
      const response = await fetch(`${API_BASE}/reply`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setReplies(prev => ({ ...prev, [index]: data.reply || 'No reply generated' }));
    } catch (err) {
      console.error('Reply generation failed:', err);
      alert('Error generating reply');
    }
  };

  const handleExpand = (index, snippet) => {
    const isExpanded = index === expandedIndex;
    setExpandedIndex(isExpanded ? null : index);

    if (!isExpanded) {
      if (!summaries[index]) handleSummarize(snippet, index);
      if (!replies[index]) generateReply(snippet, index);
    }
  };

  return (
    <div className="container">
      <h1>📬 Email Summarizer + Smart Reply</h1>

      {!accessToken ? (
        <button className="login-btn" onClick={login}>Login with Google</button>
      ) : (
        <>
          <button className="fetch-btn" onClick={fetchEmails}>📩 Fetch Email Threads</button>

          <ul className="email-list">
            {emails.map((email, index) => (
              <li key={index} className="email-item">
                <p><strong>From:</strong> {email.from}</p>
                <p><strong>Subject:</strong> {email.subject}</p>
                <p><strong>Snippet:</strong> {email.snippet}</p>

                <button className="thread-btn" onClick={() => handleExpand(index, email.snippet)}>
                  {expandedIndex === index ? '🔽 Hide Thread' : '🔍 View Thread'}
                </button>

                {expandedIndex === index && (
                  <div className="summary-box">
                    <div className="summary-section">
                      <h3>📝 Email Summary</h3>
                      <p>{loadingIndex === index ? 'Summarizing…' : summaries[index]}</p>
                    </div>

                    <div className="reply-section">
                      <h3>💬 Smart Reply</h3>
                      <p>{replies[index] || 'Generating reply…'}</p>
                    </div>
                  </div>
                )}
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

export default function App() {
  return (
    <GoogleOAuthProvider clientId="537746258088-hodk58cd7b0ul1tipbu5nhoskeuuvbau.apps.googleusercontent.com">
      <GmailReader />
    </GoogleOAuthProvider>
  );
}
