#include "Auxiliary/interface/Table.h"
#include <iomanip>  // std::setprecision
#include <iostream>
#include <fstream>

//****************************************************************************
Table::Table(std::string titleRow, 
	     std::string format,
	     std::string tableSpecs)
//****************************************************************************
{

  // Ensure that title row always starts with an empty character
  if ( titleRow.find(" ") != 0 ) titleRow = " " + titleRow;

  // Initialise object variables
  InitVars(titleRow, format, tableSpecs);
  
}


//****************************************************************************
void Table::InitVars(std::string titleRow, 
		     std::string format,
		     std::string tableSpecs)
//****************************************************************************
{
  
  // Initialise internal variable values
  bCalledPrintAux_ = false;

  // Save settings to internal variables  
  format_     = format;
  titleRow    += rowEnd_;
  tableSpecs_ = tableSpecs;

  // Setup the table format: 'LaTeX' or 'Text'
  titleRow = _SetupFormat(titleRow);

  // Save the title row and title column
  m_RowToString[-1] = titleRow;
  for (int c = 0; c < GetColumnsInString(titleRow); c++) m_RowColumnToString[-1][c] = GetColumnInRow(titleRow, c);

  // Set the table width
  tableWidth_ = titleRow.length() + 2*GetNumberOfColumns();
    
  return;
}



//****************************************************************************
std::string Table::_SetupFormat(std::string titleRow)
//****************************************************************************
{

  // Check that table format is ok
  if (format_.compare("LaTeX") == 0)
    {
      _ConvertTitleRowToLatex(titleRow);
      _FindStringInString("&", titleRow);
      _SetupLatex();
    }
  else if (format_.compare("Text") == 0)
    {
      _FindStringInString("|", titleRow);
      _SetupText();
    }
  else
    {
      std::cout << "E R R O R ! Table::Table(...) - Unknown table format \"" << format_ << "\""
	   << "\nPlease select \"LaTeX\" or \"Text\".\n EXIT" << std::endl;
      exit(1);
    }

  return titleRow;
}



//****************************************************************************
void Table::_FindStringInString(std::string stringToFind, 
			       std::string stringToSearch)
//****************************************************************************
{

  size_t found = stringToSearch.find(stringToFind);
  if (found == std::string::npos)
    {
      std::cout << "E R R O R ! Table::_FindStringInString_(...) Could not find string \"" << stringToFind << "\" inside string \"" << stringToSearch << "\". "
	   << "EXIT" << std::endl;
      exit(1);
    }
  return;
}

  
//****************************************************************************
void Table::_AppendRowEndToEachRow(void)
//****************************************************************************
  {
    int lastColumn = GetNumberOfColumns()-1;
    for(int iRow = -1; iRow < GetNumberOfRows(); iRow++) SetColumnForRow( iRow, lastColumn, m_RowColumnToString[iRow][lastColumn] + rowEnd_);
    
    return;
  }

    

//****************************************************************************
int Table::_GetNumberOfCharacters(std::string text)
//****************************************************************************
{
  
  int counter = 0;
  for (size_t i = 0; i < text.size(); i++) counter++;

  return counter;
}


//****************************************************************************
void Table::_SetupLatex(void)
//****************************************************************************
{

  delimiter_   = "&";
  rowEnd_      = " \\\\";
  hLine_       = "\\hline";
  commentLine_ = std::string(20, '%');  

  return;
}


//****************************************************************************
void Table::_SetupText(void)
//****************************************************************************
{

  delimiter_   = "|";
  rowEnd_      = ""; 
  hLine_       = std::string(20, '=');
  commentLine_ = std::string(20, '%');
  
  return;
}


//****************************************************************************
void Table::AddRowColumn(int iRow,
			 std::string text)
//****************************************************************************
{
  // Sanity check
  _IsValidNewRowIndex(iRow);

  // Initialise variables
  std::string stringToSave = " " + text  + " ";
  int iColumn = -1;
  
  // Determine which column inded this is for the given iRow index
  bool bNewColumn = m_RowColumnToString[iRow].find( GetNumberOfColumns(iRow) ) == m_RowColumnToString[iRow].end();
  if (bNewColumn) iColumn = GetNumberOfColumns(iRow);
  else iColumn = GetNumberOfColumns(iRow)+1;
  if (0) std::cout << "=== Table::AddRowColumn(): iColumn = " << iColumn << std::endl;

  // Save the row in a [index, string] map
  m_RowToString[iRow] += stringToSave;
  if (0) std::cout << "=== Table::AddRowColumn(): m_RowToString["<<iRow<<"] = " << m_RowToString[iRow] << std::endl;
  
  // Save the new column in the [iRow, iColumn] map
  m_RowColumnToString[iRow][iColumn] = stringToSave;
  if (0) std::cout << "=== Table::AddRowColumn(): m_RowColumnToString["<<iRow<<"]["<<iColumn<<"] = " << m_RowColumnToString[iRow][iColumn] << std::endl;

  return;
}



//****************************************************************************
void Table::_BeginTabular_(void)
//****************************************************************************
{
  
  if (format_.compare("LaTeX") == 0)
    {
      for (int iColumn = 0; iColumn <= GetNumberOfColumns(); iColumn++) tableSpecs_.append(" c ");
    }  
  else if (format_.compare("Text") == 0) return;
  else
    {
      std::cout << "E R R O R ! Table::_BeginTabular(...) - Unknown table format \"" << format_ << "\""
	   << "\nPlease select \"LaTeX\" or \"Text\".\n EXIT" << std::endl;
      exit(1);
    }
  
  AddTopRow( commentLine_ );
  AddTopRow("\\begin{table}");
  AddTopRow("\\begin{center}");
  AddTopRow("\\begin{tabular}{" + tableSpecs_ + "}");
    
  return;
}


//****************************************************************************
void Table::_DetermineMaxColumnWidths(void)
//****************************************************************************
{
  
  columnWidths_.clear();

  // For-loop: All columns. Include the title;
  for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)
    {

      int columnWidth_max = -1;
      
      // For-loop: All rows (row with index -1 is the title row)
      for(int iRow = -1; iRow < GetNumberOfRows(); iRow++)
	{
	  
	  int columnWidth = m_RowColumnToString[iRow][iColumn].length();
	  if ( columnWidth > columnWidth_max ) columnWidth_max = columnWidth;
	  
	}// for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)
      
      columnWidths_.push_back(columnWidth_max);
      
    }// for(int iRow = -1; iRow < GetNumberOfRows(); iRow++)

  return;
}


//****************************************************************************
void Table::_EndTabular_(void)
//****************************************************************************
{

  if (format_.compare("LaTeX") == 0) 
    {
      AddBottomRow(hLine_);
      AddBottomRow("\\end{tabular}");
      AddBottomRow("\\end{center}");
      AddBottomRow("\\end{table}");
      AddBottomRow( commentLine_ );
    }
  else if (format_.compare("Text") == 0) 
    {
      // AddBottomRow( hLine_ );
    }
  AddBottomRow("");
  
  return;
}



//****************************************************************************
void Table::_PrintTitleRow(void)
//****************************************************************************
{

  // Print horizontal line according to table format
  PrintHorizontalLine();

  // Is the row index found in my map? If not perhaps it was deleted so skip it!
  if( IsDeletedRow(-1) ) return;
      
  // For-loop: All columns
  for (int iColumn = 0; iColumn < GetNumberOfColumns()-1; iColumn++)
    {
            
      // Is the column index found in my map? If not perhaps it was deleted so skip it!
      if( IsDeletedColumn(iColumn) ) continue;

      std::cout << std::left << std::setw( columnWidths_.at(iColumn) ) << m_RowColumnToString[-1][iColumn] << delimiter_;
    }

  // Treat the last column differently
  int lastColumn = GetNumberOfColumns()-1;
  if( IsDeletedColumn(lastColumn) ) return;
  std::cout << std::setw( columnWidths_.at(lastColumn) ) << m_RowColumnToString[-1][lastColumn] << std::endl;

  
  // Print horizontal line according to table format
  PrintHorizontalLine();
  
  return;
}



//****************************************************************************
void Table::_PrintTableRows(void)
//****************************************************************************
{

  // For-loop: All rows (rows with index -1 is the title. Don't print that row as it is printed by the _PrintTitleRow() function)
  for(int iRow = 0; iRow < GetNumberOfRows()-2; iRow++)
    {

      // Is the row index found in my map? If not perhaps it was deleted so skip it!
      if( IsDeletedRow(iRow) ) continue;
      
      // For-loop: All columns
      for(int iColumn = 0; iColumn < GetNumberOfColumns()-1; iColumn++)
	{
	  
	  // Is the column index found in my map? If not perhaps it was deleted so skip it!
	  if( IsDeletedColumn(iColumn) ) continue;
	  
	  std::string columnText = m_RowColumnToString[iRow][iColumn];
	  int textWidth     = columnWidths_.at(iColumn);
	  
	  // Print column with index iColumn, for row with index iRow
	  std::cout << std::left << std::setw(textWidth) << m_RowColumnToString[iRow][iColumn] << delimiter_;
	  
	} // for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)

      // Print last column for row with index iRow
      std::cout << std::left << std::setw(columnWidths_.at(GetNumberOfColumns()-1)) << m_RowColumnToString[iRow][GetNumberOfColumns()-1] << std::endl;
      
    }// for(int iRow = 0; iRow < GetNumberOfRows(); iRow++)

  return;
}




//****************************************************************************
void Table::ReplaceStringInTable(std::string oldText,
				 std::string newText)
//****************************************************************************
{

  // For-loop: All rows
  for(int iRow = -1; iRow < GetNumberOfRows()-1; iRow++)
    {
      
      // For-loop: All columns
      for(int iColumn = 0; iColumn < GetNumberOfColumns()-1; iColumn++)
	{
	  
	  std::string tableEntry = m_RowColumnToString[iRow][iColumn];
	  size_t pos = tableEntry.find(oldText);
	  if ( pos == std::string::npos) continue;
	  m_RowColumnToString[iRow][iColumn].replace(pos, tableEntry.length(), newText);
	  
	} // for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)

    }// for(int iRow = 0; iRow < GetNumberOfRows(); iRow++)

  return;
}



//****************************************************************************
void Table::ReplaceStringWithOccurences(int iRowStart,
					int iRowEnd,
					int iColumnStart,
					int iColumnEnd,
					std::vector<std::string> keyWords)
//****************************************************************************
{

  if ( keyWords.size() < 1) return;
  _IsValidRowIndex(iRowStart);
  _IsValidRowIndex(iRowEnd);
  _IsValidColumnIndex(iColumnStart);
  _IsValidColumnIndex(iColumnEnd);
  
  // For-loop: All rows
  for(int iRow = iRowStart; iRow <= iRowEnd; iRow++)
    {      
      std::string newTableEntry;
      
      // For-loop: All columns
      for(int iColumn = iColumnStart; iColumn <= iColumnEnd; iColumn++)
	{
	 
	  // For-loop: All user defined keywords 
	  for(int i = 0; i < (int) keyWords.size(); i++)
	    {

	      std::string tableEntry = m_RowColumnToString[iRow][iColumn];	      
	      std::string searchWord = keyWords.at(i);
	      int counter = 0;
	      size_t pos  = 0;
	      
	      // While-loop: Over row text breaking string into delimiter tokens (columns)
	      while ( (pos = tableEntry.find(searchWord) ) != std::string::npos){
		
		std::string tmp = tableEntry.substr(0, pos+searchWord.length());
		tableEntry.erase(0, tmp.length());
		counter++;
	      }
	      
	      newTableEntry += " " + std::to_string(counter) + keyWords.at(i);
	      
	    }// for(int i = 0; i < (int) keyWords.size(); i++)
	  
	  m_RowColumnToString[iRow][iColumn] = newTableEntry + " ";
	}
    }

  // Print();
  
  return;
}


//****************************************************************************
std::string Table::GetMergedColumnsInRow(int iRow,
				    int iColumnStart,
				    int iColumnEnd)
//****************************************************************************
{
  
  _IsValidRowIndex(iRow);
  _IsValidColumnIndex(iColumnStart);
  _IsValidColumnIndex(iColumnEnd);
    
  std::string mergedColumnsText;
  // For-loop: All columns
   for(int iColumn = iColumnStart; iColumn <= iColumnEnd; iColumn++)
     {
       
       mergedColumnsText += m_RowColumnToString[iRow][iColumn];
       
     }// for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)

   return mergedColumnsText;
}



//****************************************************************************
void Table::_ConvertStringToLatex(std::string &text)
//****************************************************************************
{

  // Ensure that LaTeX mode is enabled
  if (format_.compare("LaTeX") != 0) return;

  // Replace "~" with "*"
  // replace( text.begin(), text.end(), '~', '*'); 

  // Replace "_" with "\_"
  int nChars =  text.length();
  std::vector<int> v_pos;
  for (int i = 1; i < nChars; i++)
    {
      if (text.at(i) !=  '_') continue;
      v_pos.push_back(i);
    } 
  for (int j=(int) v_pos.size()-1; j>= 0; j--) text.insert( v_pos.at(j), "\\");

  return;
}


//****************************************************************************
void Table::_ConvertTitleRowToLatex(std::string &titleRow)
//****************************************************************************
{

  replace( titleRow.begin(), titleRow.end(), '|', '&'); 
  
  return;
}



//****************************************************************************
void Table::_PrintAux(void)
//****************************************************************************
{

  if(bCalledPrintAux_) return;

  tableWidth_ = std::accumulate( columnWidths_.begin(), columnWidths_.end(), 2*GetNumberOfColumns() );
  
  // Append end-of-row characters (rowEnd_)
  _AppendRowEndToEachRow();

  // Re-adjust the width of the horizontal lines to the total table width
  if (format_.compare("Text") == 0) _SetHorizontalLine( std::string(tableWidth_ , '=') );
  _SetCommentLine(std::string(tableWidth_ + rowEnd_.length() + GetNumberOfColumns()*3, '%') );

  // Make table (LaTex or Text)
  _BeginTabular_();
  _EndTabular_();

  // Re-assign value
  bCalledPrintAux_ = true;
    
  return;
}


//****************************************************************************
void Table::Print(bool bPrintHeaders)
//****************************************************************************
{

  _DetermineMaxColumnWidths();
  _PrintAux();
  if (bPrintHeaders)
    {
      _PrintRow(rowsTop_);
      _PrintTitleRow();
    }
  _PrintTableRows();
  _PrintRow(rowsBottom_);
  return;
 
}


//****************************************************************************
int Table::GetNumberOfRows(void)
//****************************************************************************
  {

    int nRows = 0;
    // For-loop: All rows
    for(int iRow = -1; iRow < (int) m_RowToString.size(); iRow++)
      {
	if( IsDeletedRow(iRow) ) continue;

	// Increment counter
	nRows++;

      }// for(int iRow = 0; iRow < GetNumberOfRows()-1; iRow++)
	  
    return nRows;
  }



//****************************************************************************
int Table::GetNumberOfColumns(int iRow)
//****************************************************************************
{

  int nColumns   = 0;
  int lastColumn = (int) m_RowColumnToString[iRow].size();
    
  // For-loop: All columns
  for(int iColumn = 0; iColumn < lastColumn; iColumn++)
    {

      // Is the column index found in my map? If not perhaps it was deleted so skip it!
      if( IsDeletedColumn(iColumn) ) continue;

      // Increment counter
      nColumns++;

    }// for(int iColumn = 0; iColumn < GetNumberOfColumns()-1; iColumn++)
	  
  return nColumns;  
}


//****************************************************************************
int Table::GetNumberOfRowsIncludingDeleted(void)
//****************************************************************************
  {
    int nRows = m_RowToString.size();
    return nRows;
  }



//****************************************************************************
int Table::GetNumberOfColumnsIncludingDeleted(int iRow)
//****************************************************************************
{
  int nColumns = m_RowColumnToString[iRow].size();
  return nColumns;  
}


  
//****************************************************************************
void Table::SaveToFile(const char *fileName,
		       const char *fileOptions)
//****************************************************************************
{

  // File Options
  // "r": read. Open file for input operations. The file must exist.
  // "w": write. Create an empty file for output operations. If a file with
  //      the same name already exists, its contents are discarded and the file is treated as a new empty file.  
  // "a": append. Open file for output at the end of a file. Output operations always write data at the end
  //      of the file, expanding it. Repositioning operations (fseek, fsetpos, rewind) are ignored. The file is created if it does not exist.
  // "r+": read/update. Open a file for update (both for input and output). The file must exist.
  // "w+": write/update. Create an empty file and open it for update (both for input and output). If a file with the same
  //       name already exists its contents are discarded and the file is treated as a new empty file.
  // "a+": append/update. Open a file for update (both for input and output) with all output operations writing data at the end of the file.
  //       Repositioning operations (fseek, fsetpos, rewind) affects the next input operations, but output operations move the position back
  //       to the end of file. The file is created if it does not exist.


  // Rdirect the std::cout output from the  screen to file with name "fileName"
  freopen(fileName, fileOptions, stdout);
  freopen(fileName, fileOptions, stderr);
  Print();

  // Close
  fclose(stdout);
  fclose(stderr);

  // Redirect the output back to the screen 
  freopen ("/dev/tty", "a", stdout);
  freopen ("/dev/tty", "a", stderr);

  return;

}



//****************************************************************************
void Table::DeleteColumn(int iColumn)
//****************************************************************************
{

  // Sanity check
  _IsValidColumnIndex(iColumn);

  // Erase the element by key (do NOT uncomment! Dependencies elsewhere!
  // for (int iRow = -1; iRow < GetNumberOfRows(); iRow++) m_RowColumnToString[iRow].erase(iColumn);
 
  // Mark the column as deleted
  deletedColumns_.push_back(iColumn);
  
  return;
}



//****************************************************************************
void Table::DeleteRow(int iRow)
//****************************************************************************
{

  // Sanity check
  _IsValidRowIndex(iRow);

  // Mark the row as deleted
  deletedRows_.push_back(iRow);
   
  return;
}
     


//****************************************************************************
void Table::PrintRow(int iRow)
//****************************************************************************
{

  // Sanity check
  _IsValidRowIndex(iRow);

  // Print the desirable 
  std::cout << m_RowToString[iRow] << std::endl;
  
  return;
}


//****************************************************************************
void Table::PrintColumn(int iColumn)
//****************************************************************************
{

  // Sanity check
  _IsValidColumnIndex(iColumn);
  
  std::string columnText;  
  // For-loop: All rows
  for(int iRow = -1; iRow < GetNumberOfRows()-1; iRow++)
    {

      // For-loop: All columns
      for(int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++)
	{
	  
	  columnText += m_RowColumnToString[iRow][iColumn];
	}
    }

  std::cout << columnText << std::endl;
  
  return;
}


//****************************************************************************
int Table::GetColumnsInString(std::string title)
//****************************************************************************
{

  int nCols  = 1;
  size_t pos = 0;
  
  // While-loop: Over row text breaking string into delimiter tokens (columns)
  while ( (pos = title.find( delimiter_) ) != std::string::npos){

    // Get current column string
    std::string tmp_text = title.substr(0, pos);
    
    title.erase(0, tmp_text.length() + delimiter_.length() );
    nCols++;
  }

  return nCols;
}



//****************************************************************************
std::string Table::GetColumnInRow(std::string rowText,
			     int iColumn)
//****************************************************************************
{
  
  // Initialise local variables
  size_t pos       = 0;
  std::vector<std::string> v_columns;
  
  // Loop over row text breaking string into delimiter tokens (columns)
  while ( (pos = rowText.find( delimiter_) ) != std::string::npos){

    // Get current column string
    std::string columnText = rowText.substr(0, pos);    
    v_columns.push_back(columnText);

    // Erase current column to move on to the next
    rowText.erase(0, columnText.length() + delimiter_.length() );
  }

  // Last column is a special case
  v_columns.push_back(rowText);

  // Get the desirable column. Delete unneeded column vector
  std::string column = v_columns.at(iColumn);
  
  return column;  
}



//****************************************************************************
void Table::_IsValidColumnIndex(int iColumn)
//****************************************************************************
{

  if ( iColumn < 0 || iColumn >= GetNumberOfColumns() )
    {
      std::cout << "E R R O R ! Table::_IsValidColumnIndex(...) - Invalid column index \"" << iColumn << "\"."
	   << " The table has valid column indices from \"0\" to \"" << GetNumberOfColumns()-1 << "\". EXIT" << std::endl;
      exit(1);
    }
  
  return;
  
}


//****************************************************************************
void Table::_IsValidRowIndex(int iRow)
//****************************************************************************
{

  if ( iRow < -1 || iRow >= GetNumberOfRows()-1 )
    {
      std::cout << "E R R O R ! Table::_IsValidRowIndex(...) - Invalid row index \"" << iRow << "\"."
	   << " The table has valid row indices from \"-1\" to \"" << GetNumberOfRows()-2 << "\". EXIT" << std::endl;
      exit(1);
    }
  
  return;
  
}



//****************************************************************************
void Table::_IsValidNewRowIndex(int iRow)
//****************************************************************************
{

  if ( iRow < -1 || iRow > GetNumberOfRows()-1 )
    {
      std::cout << "E R R O R ! Table::_IsValidNewRowIndex(...) - Invalid NEW row index \"" << iRow << "\"."
	   << " The table has valid row indices from \"-1\" to \"" << GetNumberOfRows()-2 << "\"."
	   << " The NEW index must have a value of \"" << GetNumberOfRows()-2 << "\", not \"" << iRow << "\". EXIT" << std::endl;
      exit(1);
    }
  
  return;
  
}


//****************************************************************************
std::string Table::GetRow(int iRow)
//****************************************************************************
{
  std::string row = "";
  for (int iColumn = 0; iColumn < GetNumberOfColumns()-1; iColumn++) row += m_RowColumnToString[iRow][iColumn];
  
  return row;

}


//****************************************************************************
std::string Table::GetTitleRow(void)
//****************************************************************************
{
  std::string row = "";
  int lastColumn = GetNumberOfColumns();
  for (int iColumn = 0; iColumn < GetNumberOfColumns(); iColumn++) row += m_RowColumnToString[-1][iColumn] + " | "; 
  row += m_RowColumnToString[-1][lastColumn];
  
  return row;

}



//****************************************************************************
void Table::AppendToTitleRow(std::string newString)
//****************************************************************************
{

  std::string titleRow    = m_RowToString[-1];
  std::string newTitleRow = titleRow + newString;
  // std::cout << "titleRow = " << titleRow << std::endl;
  // std::cout << "newTitleRow = " << newTitleRow << std::endl;
  m_RowToString[-1] = newTitleRow;
  return;

}
