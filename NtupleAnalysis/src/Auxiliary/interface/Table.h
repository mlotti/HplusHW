// -*- c++ -*-
#ifndef Auxiliary_Table_h
#define Auxiliary_Table_h

// System
#include <iostream>
#include <algorithm>
#include <map>
#include <vector>
#include <numeric>
#include <string>

// User
#include "Auxiliary/interface/Constants.h"

using namespace constants;

// Type definitions
typedef std::map<int, std::string> m_Row_To_String;
typedef std::map<int, std::string>::iterator it_Row_To_String;
typedef std::map<int, std::vector<int> > m_Row_To_Rows;
typedef std::map<int, m_Row_To_String> m_RowColumn_To_String;
typedef std::map<int, m_Row_To_String>::iterator it_RowColumn_To_String;


class Table{

 public:
  // Default and overloaded constructors & destructors
  Table() {}; 
  Table(std::string titleRow, std::string format, std::string tableSpecs="");
  ~Table() {};

  // Member Functions
  void SetColumnForRow(int iRow, int iColumn, std::string newText){ m_RowColumnToString[iRow][iColumn] = newText; }
  std::string GetRow(int iRow);
  std::string GetColumnForRow(int iRow, int iColumn){ return m_RowColumnToString[iRow][iColumn]; }
  std::string GetColumnInRow(std::string rowText, int iColumn);
  std::string GetMergedColumnsInRow(int iRow, int iColumnStart, int iColumnEnd);
  std::string GetTableFormat(void){return format_;}
  std::string GetTitleRow(void);
  void AppendToTitleRow(std::string);
  int GetColumnsInString(std::string title);
  int GetNumberOfColumns(int iRow=-1);
  int GetNumberOfColumnsIncludingDeleted(int iRow=-1);
  int GetNumberOfRows(void);
  int GetNumberOfRowsIncludingDeleted(void);
  bool IsDeletedColumn(int iColumn){ return find(deletedColumns_.begin(), deletedColumns_.end(), iColumn) != deletedColumns_.end(); }
  bool IsDeletedRow(int iRow){ return find(deletedRows_.begin(), deletedRows_.end(), iRow) != deletedRows_.end(); }
  void AddBottomRow(std::string text){ rowsBottom_.push_back(text); }
  void AddRowColumn(int iRow, std::string text);
  void AddTopRow(std::string text){ rowsTop_.push_back(text); }
  void ConvertToFinalState(void);
  void DeleteColumn(int iColumn);
  void DeleteRow(int iRow);
  void InitVars(std::string titleRow, std::string format, std::string tableSpecs="");
  void Print(bool bPrintHeaders=true);
  void PrintColumn(int iColumn=-1);
  void PrintHorizontalLine(void){ std::cout << hLine_ << std::endl; } 
  void PrintRow(int iRow=-1);
  void ReplaceStringInTable(std::string before, std::string after);
  void ReplaceStringWithOccurences(int iRowStart, int iRowEnd, int iColumnStart, int iColumnEnd, std::vector<std::string> keyWords);
  void SaveToFile(const char *fileName, const char *fileOptions);
  void SetTableWidth(int width){ tableWidth_ = width; } 
    
  
  private:
  // Member Functions
  int _GetColumnWidthForRow(int iRow, int iColumn){ return GetColumnForRow(iRow, iColumn).length(); }
  int _GetNumberOfCharacters(std::string text);
  std::string _SetupFormat(std::string titleRow);
  void _AppendRowEndToEachRow(void);
  void _BeginTabular_(void);
  void _ConvertStringToLatex(std::string &text);
  void _ConvertTitleRowToLatex(std::string &titleRow);
  void _DetermineMaxColumnWidths(void);
  void _EndTabular_(void);
  void _FindStringInString(std::string stringToFind, std::string stringToSearch);
  void _IsValidColumnIndex(int iColumn);
  void _IsValidRowIndex(int iRow);
  void _IsValidNewRowIndex(int iRow);
  void _PrintAux(void);
  void _PrintRow(std::vector<std::string> row){ for (size_t i = 0; i < row.size(); i++){ std::cout << row.at(i) << std::endl;} }
  void _PrintTableRows(void);
  void _PrintTitleRow(void);
  void _SetCommentLine(std::string text){ commentLine_ = text; }
  void _SetDelimiter(std::string text){ delimiter_ = text; }
  void _SetHorizontalLine(std::string text){ hLine_ = text; }
  void _SetRowEnd(std::string text){ rowEnd_ = text; }
  void _SetTableSpecs(std::string text){ tableSpecs_ = text; }
  void _SetupLatex(void);
  void _SetupText(void);
  
  // Variables  
  bool bCalledPrintAux_;
  int tableWidth_;
  std::string format_;
  std::string tableSpecs_;
  std::string delimiter_;
  std::string rowEnd_;
  std::string hLine_;
  std::string commentLine_;
  std::vector<std::string> rowsTop_; 
  std::vector<std::string> rowsBottom_;
  std::vector<int> columnWidths_;
  std::vector<int> deletedRows_;
  std::vector<int> deletedColumns_;
  m_Row_To_String m_RowToString;
  m_RowColumn_To_String m_RowColumnToString;

};

#endif
