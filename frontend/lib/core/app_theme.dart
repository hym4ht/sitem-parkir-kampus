import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // === Color Palette ===
  static const Color primary = Color(0xFF800000); // Maroon
  static const Color maroon = primary; // Backward compatibility
  static const Color maroonDark = primary;
  static const Color maroonLight = primary;
  static const Color maroonSurface = Color(0xFFF9FAFB);
  static const Color background = Color(0xFFFFFFFF); // Putih bersih
  static const Color surfaceAccent = Color(0xFFF9FAFB); // Abu-abu sangat muda
  static const Color bodyText = Colors.black87; // Body text color

  // Accent & Semantic Colors
  static const Color gold = Color(0xFFD4A843);
  static const Color goldLight = Color(0xFFF5C842);
  static const Color teal = Color(0xFF0EA5E9);
  static const Color tealLight = Color(0xFFE0F2FE);
  static const Color emerald = Color(0xFF10B981);
  static const Color amber = Color(0xFFF59E0B);
  static const Color slate50 = Color(0xFFF8FAFC);
  static const Color slate100 = Color(0xFFF1F5F9);
  static const Color slate200 = Color(0xFFE2E8F0);
  static const Color slate500 = Color(0xFF64748B);
  static const Color slate700 = Color(0xFF334155);
  static const Color slate900 = Color(0xFF0F172A);

  static ThemeData get theme {
    final textTheme = GoogleFonts.plusJakartaSansTextTheme().copyWith(
      displayLarge: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      displayMedium: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      displaySmall: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      headlineLarge: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      headlineMedium: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      headlineSmall: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      titleLarge: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      titleMedium: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      titleSmall: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800, letterSpacing: -1.0, color: bodyText),
      bodyLarge: GoogleFonts.plusJakartaSans(color: bodyText),
      bodyMedium: GoogleFonts.plusJakartaSans(color: bodyText),
      bodySmall: GoogleFonts.plusJakartaSans(color: bodyText),
    );

    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: primary,
        primary: primary,
        surface: background,
        surfaceContainerHighest: surfaceAccent,
        onSurface: bodyText,
        brightness: Brightness.light,
      ),
      textTheme: textTheme,
      scaffoldBackgroundColor: background,

      // AppBar
      appBarTheme: AppBarTheme(
        backgroundColor: background,
        foregroundColor: primary,
        elevation: 0,
        scrolledUnderElevation: 0,
        centerTitle: false,
        titleTextStyle: GoogleFonts.plusJakartaSans(
          color: primary,
          fontSize: 20,
          fontWeight: FontWeight.w800,
          letterSpacing: -1.0,
        ),
        iconTheme: const IconThemeData(color: primary),
      ),

      // Cards
      cardTheme: CardThemeData(
        color: surfaceAccent,
        elevation: 0,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8.0),
          side: const BorderSide(color: Color(0xFFE5E7EB), width: 1.0),
        ),
        margin: EdgeInsets.zero,
      ),

      // Elevated Button
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          elevation: 0,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          textStyle: GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w700),
        ),
      ),

      // Filled Button
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: primary,
          foregroundColor: Colors.white,
          elevation: 0,
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          textStyle: GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w700),
        ),
      ),

      // Outlined Button
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: primary,
          side: const BorderSide(color: primary, width: 1.5),
          shape:
              RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
          textStyle: GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w700),
        ),
      ),

      // Input fields
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceAccent,
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(color: Color(0xFFE5E7EB)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(color: Color(0xFFE5E7EB)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(8.0),
          borderSide: const BorderSide(color: primary, width: 2.0),
        ),
        labelStyle: GoogleFonts.plusJakartaSans(color: Colors.black54),
        hintStyle: GoogleFonts.plusJakartaSans(color: Colors.black38),
      ),

      // Bottom Nav
      bottomNavigationBarTheme: BottomNavigationBarThemeData(
        backgroundColor: background,
        selectedItemColor: primary,
        unselectedItemColor: Colors.black54,
        selectedLabelStyle:
            GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w800),
        unselectedLabelStyle:
            GoogleFonts.plusJakartaSans(fontWeight: FontWeight.w500),
        elevation: 0,
        type: BottomNavigationBarType.fixed,
      ),

      // FloatingActionButton
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: primary,
        foregroundColor: Colors.white,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
      ),

      // Chip
      chipTheme: ChipThemeData(
        backgroundColor: surfaceAccent,
        labelStyle: GoogleFonts.plusJakartaSans(
            color: primary, fontWeight: FontWeight.w600),
        side: const BorderSide(color: Color(0xFFE5E7EB)),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
      ),

      // Divider
      dividerTheme: const DividerThemeData(
          color: Color(0xFFE5E7EB), thickness: 1, space: 1),

      // Dialog
      dialogTheme: DialogThemeData(
        backgroundColor: background,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8.0)),
        elevation: 0,
        titleTextStyle: GoogleFonts.plusJakartaSans(
          fontWeight: FontWeight.w800,
          letterSpacing: -1.0,
          color: bodyText,
          fontSize: 20,
        ),
        contentTextStyle: GoogleFonts.plusJakartaSans(color: bodyText),
      ),
    );
  }

  static BoxDecoration get modernCard => BoxDecoration(
        color: surfaceAccent,
        borderRadius: BorderRadius.circular(8.0),
        border: Border.all(color: const Color(0xFFE5E7EB), width: 1.0),
      );

  static BoxDecoration get headerGradient => const BoxDecoration(
        color: primary,
      );

  static BoxDecoration get glassCard => BoxDecoration(
        color: surfaceAccent,
        borderRadius: BorderRadius.circular(8.0),
        border: Border.all(color: const Color(0xFFE5E7EB), width: 1.0),
      );

  // Status colors
  static Color statusColor(String status) {
    switch (status.toLowerCase()) {
      case 'disetujui':
        return const Color(0xFF10B981); // emerald
      case 'ditolak':
        return const Color(0xFFDC2626); // red
      case 'pending':
        return const Color(0xFFF59E0B); // amber
      default:
        return Colors.black54;
    }
  }

  static IconData statusIcon(String status) {
    switch (status.toLowerCase()) {
      case 'disetujui':
        return Icons.check_circle_outline;
      case 'ditolak':
        return Icons.highlight_off;
      case 'pending':
        return Icons.hourglass_empty;
      default:
        return Icons.info_outline;
    }
  }
}
