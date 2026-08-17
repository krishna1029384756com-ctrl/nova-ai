package com.nova.companion

import android.graphics.Color
import android.graphics.Typeface
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.*
import androidx.activity.ComponentActivity

class MainActivity : ComponentActivity() {

    private val bg = Color.rgb(10, 11, 16)
    private val card = Color.rgb(20, 21, 29)
    private val card2 = Color.rgb(27, 28, 38)
    private val primary = Color.rgb(124, 92, 255)
    private val text = Color.rgb(242, 242, 248)
    private val muted = Color.rgb(155, 157, 172)
    private val green = Color.rgb(67, 210, 145)

    private lateinit var statusText: TextView
    private lateinit var statusDot: TextView
    private lateinit var connectButton: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        buildUi()
    }

    private fun dp(v: Int): Int = (v * resources.displayMetrics.density).toInt()

    private fun textView(
        value: String,
        size: Float,
        color: Int,
        bold: Boolean = false
    ) = TextView(this).apply {
        text = value
        textSize = size
        setTextColor(color)
        typeface = if (bold) Typeface.create("sans", Typeface.BOLD) else Typeface.create("sans", Typeface.NORMAL)
    }

    private fun rounded(color: Int, radius: Float): android.graphics.drawable.GradientDrawable =
        android.graphics.drawable.GradientDrawable().apply {
            setColor(color)
            cornerRadius = dp(radius.toInt()).toFloat()
        }

    private fun buildUi() {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(bg)
            setPadding(dp(20), dp(18), dp(20), dp(18))
        }

        // Header
        val header = LinearLayout(this).apply {
            gravity = Gravity.CENTER_VERTICAL
        }

        val logo = TextView(this).apply {
            text = "N"
            textSize = 20f
            gravity = Gravity.CENTER
            setTextColor(Color.WHITE)
            typeface = Typeface.DEFAULT_BOLD
            background = rounded(primary, 13f)
        }
        header.addView(logo, LinearLayout.LayoutParams(dp(46), dp(46)))

        val titleBox = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(12), 0, 0, 0)
        }
        titleBox.addView(textView("NOVA Companion", 20f, text, true))
        titleBox.addView(textView("Phone control bridge", 13f, muted))
        header.addView(titleBox, LinearLayout.LayoutParams(0, -2, 1f))

        val version = textView("v0.1", 12f, muted).apply {
            setPadding(dp(10), dp(6), dp(10), dp(6))
            background = rounded(card2, 12f)
        }
        header.addView(version)
        root.addView(header)

        // Main connection card
        val connectionCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(18))
            background = rounded(card, 20f)
        }
        val cardTitle = textView("Connection", 16f, text, true)
        connectionCard.addView(cardTitle)

        val statusRow = LinearLayout(this).apply {
            gravity = Gravity.CENTER_VERTICAL
            setPadding(0, dp(14), 0, dp(4))
        }
        statusDot = textView("●", 18f, muted)
        statusRow.addView(statusDot, LinearLayout.LayoutParams(dp(28), -2))
        statusText = textView("Not connected", 16f, muted, true)
        statusRow.addView(statusText)
        connectionCard.addView(statusRow)

        val detail = textView(
            "The companion stays idle until you start a session.",
            13f, muted
        )
        detail.setPadding(0, dp(2), 0, dp(16))
        connectionCard.addView(detail)

        connectButton = textView("START CONNECTION", 14f, Color.WHITE, true).apply {
            gravity = Gravity.CENTER
            setPadding(0, dp(14), 0, dp(14))
            background = rounded(primary, 16f)
            isClickable = true
            setOnClickListener {
                // Milestone 0: UI only. LAN discovery is the next module.
                statusDot.setTextColor(green)
                statusText.text = "Ready for connection"
                statusText.setTextColor(text)
                text = "CONNECTION MODULE NEXT"
                alpha = 0.65f
                isClickable = false
            }
        }
        connectionCard.addView(connectButton, LinearLayout.LayoutParams(-1, dp(52)))
        root.addView(connectionCard, LinearLayout.LayoutParams(-1, -2).apply {
            topMargin = dp(26)
        })

        // Device card
        val deviceCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(18))
            background = rounded(card, 20f)
        }
        deviceCard.addView(textView("This device", 16f, text, true))
        deviceCard.addView(textView("Android Companion", 14f, muted).apply {
            setPadding(0, dp(10), 0, dp(3))
        })
        deviceCard.addView(textView("Waiting for NOVA on your PC", 13f, muted))
        root.addView(deviceCard, LinearLayout.LayoutParams(-1, -2).apply {
            topMargin = dp(14)
        })

        // Protocol card
        val protocolCard = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(dp(18), dp(18), dp(18), dp(18))
            background = rounded(card, 20f)
        }
        protocolCard.addView(textView("Current milestone", 16f, text, true))
        protocolCard.addView(textView("LAN discovery  →  pair  →  PING / PONG", 14f, muted).apply {
            setPadding(0, dp(10), 0, 0)
        })
        protocolCard.addView(textView("No AI • No file transfer • No always-on service", 12f, muted).apply {
            setPadding(0, dp(7), 0, 0)
        })
        root.addView(protocolCard, LinearLayout.LayoutParams(-1, -2).apply {
            topMargin = dp(14)
        })

        val footer = textView("NOVA • On-demand phone control", 12f, muted).apply {
            gravity = Gravity.CENTER
        }
        root.addView(footer, LinearLayout.LayoutParams(-1, 0, 1f).apply {
            gravity = Gravity.BOTTOM
        })

        setContentView(root)
    }
}
