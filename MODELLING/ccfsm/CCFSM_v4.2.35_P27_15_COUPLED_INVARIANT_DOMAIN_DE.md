# CCFSM v4.2.35 — P27.15: gekoppelter FV-Invariantenbereichs-Limiter

**Status: implementiert; CI-Prüfung ausstehend.**

P27.15 ergänzt P27.14 um einen gemeinsamen fraction-to-boundary-Limiter für den FV-Zustandsvektor
\[
x=(\theta,n_M,n_O,n_N,n_B).
\]
Für einen vorgegebenen Zustand, eine RHS-Auswertung und einen Zeitschritt wird ein gemeinsamer Faktor \(\alpha\in[0,1]\) bestimmt:
\[
x^{n+1}=x^n+\alpha\,\Delta t\,F(x^n).
\]
Die Schranken lauten \(\theta_{\min}<\theta\leq1\) und \(n_s>n_{s,\min}\). Ein gemeinsamer Faktor wirkt auf alle Zellen, theta und M/O/N/B. Der P21-Adapter liest die Transport-RHS direkt aus einem Snapshot.

**Mathematische Aussage:** Bei erfolgreicher Rückgabe erfüllt der explizite Euler-Kandidat für genau die übergebene RHS-Auswertung die angegebenen komponentenweisen Schranken. Voller und begrenzter Schritt werden unterschieden; aktive Schranken und effektive Schrittweite werden ausgewiesen.

**Keine weitergehende Behauptung:** Kein Nachweis, dass der Kandidat den impliziten P22/P24-Residual löst; kein Beweis der RHS-Konservativität, Energieabnahme, Zeitschrittstabilität, kontinuierlichen PDE-Invariantenregion oder physikalischen Gültigkeit. Der Limiter ersetzt weder Solverkonvergenz noch Modellvalidierung.

Regressionen: voller Schritt, Inventar-Untergrenze, theta-Obergrenze, ungültiger Anfangszustand/Steuerung, fehlerhafte Speziesform, P21-Adapter und explizite Nichtbehauptung von Solver-/Physikbeweisen.
