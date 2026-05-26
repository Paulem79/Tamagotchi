import express from "express";
import mysql from "mysql2/promise";
import cors from "cors";
import dotenv from "dotenv";

dotenv.config();

const app = express();
app.use(express.json());
app.use(cors());

const jdbcUrl = process.env.JDBC_URL!;
const port = process.env.PORT!;

// Regex pour clean l'url JDBC (pratique !)
const cleanUrl = jdbcUrl.replace(/^jdbc:[^:]+:\/\//, 'http://');
// Et le reste avec une méthode intégrée pour parse l'URL (je savais pas que c'était possible)
const parsed = new URL(cleanUrl);

const dbPool = mysql.createPool({
    host: parsed.hostname,
    port: parsed.port ? parseInt(parsed.port) : 3306,
    user: parsed.username ? decodeURIComponent(parsed.username) : (parsed.searchParams.get('user') || "root"),
    password: parsed.password ? decodeURIComponent(parsed.password) : (parsed.searchParams.get('password') || ""),
    database: parsed.pathname.replace(/^\//, ''),
    waitForConnections: true,
    connectionLimit: 10
});

// Récupérer le top 5
app.get("/leaderboard", async (req, res) => {
    try {
        const [rows] = await dbPool.query(
            "SELECT pseudo, score FROM leaderboard ORDER BY score DESC LIMIT 5"
        );
        res.json(rows);
    } catch (error) {
        res.status(500).json({ error: "Erreur" });
        console.error(error);
    }
});

// Ajoute un score pour pseudo et score (simple)
app.post("/score", async (req, res) => {
    const { pseudo, score } = req.body;
    try {
        await dbPool.query(
            "INSERT INTO leaderboard (pseudo, score) VALUES (?, ?)",
            [pseudo, score]
        );
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: "Erreur" });
        console.error(error);
    }
});

app.listen(port, () => {
    console.log(`API écoute sur le port ${port}`);
});